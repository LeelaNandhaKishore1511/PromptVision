import time
import cv2
import numpy as np
import pywt
from typing import Dict, Any, Tuple
from pathlib import Path
from PIL import Image

def get_stats(img_array: np.ndarray) -> Dict[str, Any]:
    return {
        "min": float(np.min(img_array)),
        "max": float(np.max(img_array)),
        "mean": round(float(np.mean(img_array)), 2),
        "std": round(float(np.std(img_array)), 2),
    }

def run_rgb_grayscale(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Converts image to grayscale and visualizes R, G, B color channels side-by-side or composite."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    b, g, r = cv2.split(img_bgr)
    
    # Create composite visualization: 2x2 grid (Original, R-channel, G-channel, B-channel)
    h, w = gray.shape[:2]
    # Downscale for collage if large
    scale = 0.5 if max(h, w) > 800 else 1.0
    if scale < 1.0:
        h_s, w_s = int(h * scale), int(w * scale)
        orig_s = cv2.resize(img_bgr, (w_s, h_s))
        r_c = cv2.applyColorMap(cv2.resize(r, (w_s, h_s)), cv2.COLORMAP_JET)
        g_c = cv2.applyColorMap(cv2.resize(g, (w_s, h_s)), cv2.COLORMAP_SUMMER)
        b_c = cv2.applyColorMap(cv2.resize(b, (w_s, h_s)), cv2.COLORMAP_OCEAN)
    else:
        orig_s = img_bgr
        r_c = cv2.applyColorMap(r, cv2.COLORMAP_JET)
        g_c = cv2.applyColorMap(g, cv2.COLORMAP_SUMMER)
        b_c = cv2.applyColorMap(b, cv2.COLORMAP_OCEAN)
        
    top_row = np.hstack([orig_s, r_c])
    bot_row = np.hstack([g_c, b_c])
    collage = np.vstack([top_row, bot_row])
    
    # Metadata
    metadata = {
        "channel_count": 3,
        "color_space": "BGR / RGB",
        "r_channel_stats": get_stats(r),
        "g_channel_stats": get_stats(g),
        "b_channel_stats": get_stats(b),
        "grayscale_stats": get_stats(gray),
        "description": "Composite visualization displaying Original (top-left), Red intensity heatmap (top-right), Green heatmap (bottom-left), and Blue heatmap (bottom-right)."
    }
    return collage, metadata

def run_pixel_inspection(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Pixel intensity inspection, entropy, distribution, and overlay of intensity heatmap."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # Calculate Shannon Entropy
    hist, _ = np.histogram(gray, bins=256, range=(0, 256), density=True)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))
    
    # Heatmap overlay
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_VIRIDIS)
    blended = cv2.addWeighted(img_bgr, 0.4, heatmap, 0.6, 0)
    
    metadata = {
        "dimensions": f"{w}x{h}",
        "total_pixels": int(w * h),
        "shannon_entropy": round(float(entropy), 3),
        "mean_intensity": round(float(np.mean(gray)), 2),
        "std_intensity": round(float(np.std(gray)), 2),
        "min_intensity": int(np.min(gray)),
        "max_intensity": int(np.max(gray)),
        "dynamic_range": int(np.max(gray) - np.min(gray)),
        "description": "Intensity inspection with Viridis colormap overlay showing intensity distribution and Shannon information entropy."
    }
    return blended, metadata

def run_sampling_demonstration(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Demonstrates Nyquist-Shannon sampling theorem, showing downsampling aliasing vs anti-aliased decimation."""
    factor = int(params.get("factor", 4))
    if factor not in [2, 4, 8, 16]:
        factor = 4
        
    h, w = img_bgr.shape[:2]
    new_w, new_h = max(1, w // factor), max(1, h // factor)
    
    # Aliased: direct nearest neighbor downsampling without pre-filtering
    down_aliased = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    up_aliased = cv2.resize(down_aliased, (w, h), interpolation=cv2.INTER_NEAREST)
    
    # Anti-aliased: Gaussian low-pass pre-filtering prior to decimation
    sigma = factor / 2.0
    ksize = int(2 * round(3 * sigma) + 1)
    if ksize % 2 == 0:
        ksize += 1
    blurred = cv2.GaussianBlur(img_bgr, (ksize, ksize), sigma)
    down_filtered = cv2.resize(blurred, (new_w, new_h), interpolation=cv2.INTER_AREA)
    up_filtered = cv2.resize(down_filtered, (w, h), interpolation=cv2.INTER_LINEAR)
    
    # Side-by-side comparison
    label_font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(up_aliased, f"Subsampled {factor}x (No Anti-Aliasing)", (20, 40), label_font, 0.8, (0, 0, 255), 2)
    cv2.putText(up_filtered, f"Anti-Aliased {factor}x (Gaussian Preserved)", (20, 40), label_font, 0.8, (0, 255, 0), 2)
    
    comparison = np.hstack([up_aliased, up_filtered])
    
    # Mean squared difference between aliased and anti-aliased
    diff = float(np.mean((up_aliased.astype(float) - up_filtered.astype(float)) ** 2))
    
    metadata = {
        "downsampling_factor": factor,
        "original_resolution": f"{w}x{h}",
        "sampled_resolution": f"{new_w}x{new_h}",
        "aliasing_distortion_mse": round(diff, 2),
        "nyquist_rate_comment": f"High frequencies above Nyquist limit (fs/{factor*2}) fold back as moiré and staircasing artifacts unless low-pass pre-filtered.",
        "description": "Side-by-side sampling comparison: Aliased decimation (left) vs Anti-aliased filtered reconstruction (right)."
    }
    return comparison, metadata

def run_fourier_transform(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Computes 2D Discrete Fourier Transform (FFT) and visualizes the log magnitude spectrum."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # Compute 2D FFT and shift zero-frequency component to center
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    
    # Log magnitude spectrum
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-6)
    norm_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Colorize spectrum
    spectrum_colored = cv2.applyColorMap(norm_spectrum, cv2.COLORMAP_INFERNO)
    
    # Combine original grayscale (in 3 channels) and Fourier spectrum
    gray_3c = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.putText(gray_3c, "Spatial Domain (f(x, y))", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(spectrum_colored, "Frequency Spectrum (F(u, v))", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    combined = np.hstack([gray_3c, spectrum_colored])
    
    # Measure dominant energy ratio (DC component vs high frequency energy)
    total_energy = float(np.sum(np.abs(fshift)**2))
    center_y, center_x = h // 2, w // 2
    r = min(h, w) // 10
    low_freq_mask = np.zeros((h, w), dtype=bool)
    y_idx, x_idx = np.ogrid[:h, :w]
    low_freq_mask[(y_idx - center_y)**2 + (x_idx - center_x)**2 <= r**2] = True
    low_freq_energy = float(np.sum(np.abs(fshift[low_freq_mask])**2))
    low_freq_ratio = round((low_freq_energy / (total_energy + 1e-9)) * 100, 2)
    
    metadata = {
        "fft_dimensions": f"{w}x{h}",
        "low_frequency_energy_percentage": low_freq_ratio,
        "high_frequency_energy_percentage": round(100.0 - low_freq_ratio, 2),
        "dominant_frequencies": "Concentrated near DC origin (smooth structures)" if low_freq_ratio > 80 else "Rich in high frequency textures and edges",
        "description": "2D Fast Fourier Transform log magnitude spectrum showing spatial frequency distribution."
    }
    return combined, metadata

def run_wavelet_decomposition(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """2D Discrete Wavelet Transform (Haar Wavelet) producing LL, LH, HL, HH subbands."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Perform 2D Haar DWT
    coeffs2 = pywt.dwt2(gray, 'haar')
    LL, (LH, HL, HH) = coeffs2
    
    def norm_band(band):
        return cv2.normalize(np.abs(band), None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        
    ll_img = norm_band(LL)
    lh_img = norm_band(LH)
    hl_img = norm_band(HL)
    hh_img = norm_band(HH)
    
    # Add titles to subbands
    font = cv2.FONT_HERSHEY_SIMPLEX
    ll_c = cv2.cvtColor(ll_img, cv2.COLOR_GRAY2BGR)
    lh_c = cv2.cvtColor(lh_img, cv2.COLOR_GRAY2BGR)
    hl_c = cv2.cvtColor(hl_img, cv2.COLOR_GRAY2BGR)
    hh_c = cv2.cvtColor(hh_img, cv2.COLOR_GRAY2BGR)
    
    cv2.putText(ll_c, "LL (Approx / Low-Low)", (15, 30), font, 0.6, (0, 255, 0), 2)
    cv2.putText(lh_c, "LH (Horizontal Detail)", (15, 30), font, 0.6, (0, 255, 255), 2)
    cv2.putText(hl_c, "HL (Vertical Detail)", (15, 30), font, 0.6, (0, 255, 255), 2)
    cv2.putText(hh_c, "HH (Diagonal Detail)", (15, 30), font, 0.6, (0, 255, 255), 2)
    
    top = np.hstack([ll_c, lh_c])
    bot = np.hstack([hl_c, hh_c])
    wavelet_grid = np.vstack([top, bot])
    
    metadata = {
        "wavelet_family": "Haar (db1)",
        "decomposition_levels": 1,
        "subband_dimensions": f"{LL.shape[1]}x{LL.shape[0]}",
        "energy_ll": round(float(np.sum(LL**2)), 1),
        "energy_lh": round(float(np.sum(LH**2)), 1),
        "energy_hl": round(float(np.sum(HL**2)), 1),
        "energy_hh": round(float(np.sum(HH**2)), 1),
        "description": "2D Haar Wavelet Decomposition displaying LL approximation, LH horizontal subband, HL vertical subband, and HH diagonal high-frequency subband."
    }
    return wavelet_grid, metadata
