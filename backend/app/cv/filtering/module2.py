import cv2
import numpy as np
from typing import Dict, Any, Tuple
import io
from PIL import Image

def run_averaging_filter(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    ksize = int(params.get("kernel_size", 5))
    if ksize % 2 == 0:
        ksize += 1
    ksize = max(3, min(ksize, 31))
    
    blurred = cv2.blur(img_bgr, (ksize, ksize))
    
    # Calculate noise reduction metric (gradient reduction)
    grad_orig = np.mean(np.abs(cv2.Sobel(img_bgr, cv2.CV_64F, 1, 1)))
    grad_blur = np.mean(np.abs(cv2.Sobel(blurred, cv2.CV_64F, 1, 1)))
    smoothing_factor = round(float((1 - grad_blur / (grad_orig + 1e-6)) * 100), 2)
    
    metadata = {
        "filter": "Linear Box/Averaging Filter",
        "kernel_size": f"{ksize}x{ksize}",
        "smoothing_percentage": smoothing_factor,
        "description": f"Applied {ksize}x{ksize} uniform spatial convolution filter for high-frequency noise suppression."
    }
    return blurred, metadata

def run_gaussian_filter(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    ksize = int(params.get("kernel_size", 7))
    if ksize % 2 == 0:
        ksize += 1
    ksize = max(3, min(ksize, 31))
    sigma = float(params.get("sigma", 1.5))
    
    blurred = cv2.GaussianBlur(img_bgr, (ksize, ksize), sigma)
    
    metadata = {
        "filter": "Gaussian Smoothing Filter",
        "kernel_size": f"{ksize}x{ksize}",
        "sigma": sigma,
        "description": f"Applied 2D Gaussian kernel with standard deviation sigma={sigma} for isotropic frequency attenuation."
    }
    return blurred, metadata

def run_median_filter(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    ksize = int(params.get("kernel_size", 5))
    if ksize % 2 == 0:
        ksize += 1
    ksize = max(3, min(ksize, 31))
    
    filtered = cv2.medianBlur(img_bgr, ksize)
    
    metadata = {
        "filter": "Median Non-Linear Filter",
        "kernel_size": ksize,
        "salt_and_pepper_robustness": "High (order-statistic filter)",
        "description": f"Non-linear median filtering with {ksize}x{ksize} window for impulse noise elimination without blurring sharp boundaries."
    }
    return filtered, metadata

def run_bilateral_filter(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    d = int(params.get("diameter", 9))
    sigma_color = float(params.get("sigma_color", 75))
    sigma_space = float(params.get("sigma_space", 75))
    
    filtered = cv2.bilateralFilter(img_bgr, d, sigma_color, sigma_space)
    
    metadata = {
        "filter": "Bilateral Edge-Preserving Filter",
        "diameter": d,
        "sigma_color": sigma_color,
        "sigma_space": sigma_space,
        "description": "Combines spatial Euclidean distance and photometric radiometric differences to smooth textures while strictly preserving salient edges."
    }
    return filtered, metadata

def run_thresholding(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    mode = str(params.get("mode", "otsu")).lower() # binary, adaptive_mean, adaptive_gaussian, otsu
    cutoff = int(params.get("cutoff", 127))
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    if mode == "binary":
        _, thresh = cv2.threshold(gray, cutoff, 255, cv2.THRESH_BINARY)
        actual_thresh = cutoff
        desc = f"Global binary thresholding at fixed intensity value {cutoff}."
    elif mode == "adaptive_mean":
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        actual_thresh = "Locally Adaptive Mean"
        desc = "Local adaptive mean thresholding accounting for non-uniform illumination."
    elif mode == "adaptive_gaussian":
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        actual_thresh = "Locally Adaptive Gaussian"
        desc = "Local adaptive Gaussian weighted thresholding."
    else: # Otsu
        actual_thresh, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        actual_thresh = round(float(actual_thresh), 1)
        desc = f"Otsu's optimal clustering threshold computed at intensity {actual_thresh}."
        
    white_pixels = int(np.count_nonzero(thresh == 255))
    total_pixels = thresh.size
    foreground_ratio = round((white_pixels / total_pixels) * 100, 2)
    
    thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    metadata = {
        "thresholding_mode": mode,
        "calculated_threshold_value": actual_thresh,
        "foreground_pixel_ratio_pct": foreground_ratio,
        "background_pixel_ratio_pct": round(100.0 - foreground_ratio, 2),
        "description": desc
    }
    return thresh_bgr, metadata

def run_morphological_ops(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    op_name = str(params.get("operation", "opening")).lower() # erosion, dilation, opening, closing
    ksize = int(params.get("kernel_size", 5))
    if ksize % 2 == 0:
        ksize += 1
    iterations = int(params.get("iterations", 1))
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    
    if op_name == "erosion":
        res = cv2.erode(img_bgr, kernel, iterations=iterations)
        desc = f"Morphological erosion with {ksize}x{ksize} rectangular structuring element ({iterations} iter)."
    elif op_name == "dilation":
        res = cv2.dilate(img_bgr, kernel, iterations=iterations)
        desc = f"Morphological dilation expanding bright structural features ({iterations} iter)."
    elif op_name == "opening":
        res = cv2.morphologyEx(img_bgr, cv2.MORPH_OPEN, kernel, iterations=iterations)
        desc = f"Morphological opening (erosion followed by dilation) removing isolated foreground noise."
    else: # closing
        res = cv2.morphologyEx(img_bgr, cv2.MORPH_CLOSE, kernel, iterations=iterations)
        desc = f"Morphological closing (dilation followed by erosion) bridging narrow gaps and filling holes."
        
    metadata = {
        "operation": op_name,
        "structuring_element": f"RECT {ksize}x{ksize}",
        "iterations": iterations,
        "description": desc
    }
    return res, metadata

def run_histogram_equalization(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    method = str(params.get("method", "clahe")).lower() # global, clahe
    
    # Convert to YCrCb to equalize intensity/luminance channel without corrupting chromaticity
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    
    if method == "global":
        y_eq = cv2.equalizeHist(y)
        desc = "Global histogram equalization stretching full dynamic range across cumulative distribution function."
    else: # CLAHE
        clip_limit = float(params.get("clip_limit", 2.5))
        tile_size = int(params.get("tile_size", 8))
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
        y_eq = clahe.apply(y)
        desc = f"Contrast Limited Adaptive Histogram Equalization (CLAHE, clip={clip_limit}, tile={tile_size}x{tile_size}) preventing over-amplification of noise."
        
    merged = cv2.merge([y_eq, cr, cb])
    result = cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)
    
    # Compare contrast variance
    std_before = round(float(np.std(y)), 2)
    std_after = round(float(np.std(y_eq)), 2)
    
    metadata = {
        "equalization_method": method,
        "luminance_std_before": std_before,
        "luminance_std_after": std_after,
        "contrast_gain_ratio": round(std_after / (std_before + 1e-6), 2),
        "description": desc
    }
    return result, metadata

def run_jpeg_compression_comparison(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Simulates DCT-based JPEG quantization and artifact creation at Q=10, Q=50, Q=90."""
    h, w = img_bgr.shape[:2]
    
    def compress_at_q(q):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), q]
        _, enc = cv2.imencode('.jpg', img_bgr, encode_param)
        dec = cv2.imdecode(enc, cv2.IMREAD_COLOR)
        size_kb = len(enc) / 1024.0
        mse = np.mean((img_bgr.astype(float) - dec.astype(float)) ** 2)
        psnr = 10 * np.log10(255.0**2 / (mse + 1e-9)) if mse > 0 else 99.0
        return dec, round(size_kb, 1), round(float(psnr), 2)
        
    img_q10, sz_10, psnr_10 = compress_at_q(10)
    img_q50, sz_50, psnr_50 = compress_at_q(50)
    img_q90, sz_90, psnr_90 = compress_at_q(90)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_q10, f"Q=10 ({sz_10}KB, PSNR {psnr_10}dB)", (15, 30), font, 0.6, (0, 0, 255), 2)
    cv2.putText(img_q50, f"Q=50 ({sz_50}KB, PSNR {psnr_50}dB)", (15, 30), font, 0.6, (0, 255, 255), 2)
    cv2.putText(img_q90, f"Q=90 ({sz_90}KB, PSNR {psnr_90}dB)", (15, 30), font, 0.6, (0, 255, 0), 2)
    
    # Scale if large
    if w > 400:
        s_w, s_h = w // 2, h // 2
        p1 = cv2.resize(img_q10, (s_w, s_h))
        p2 = cv2.resize(img_q50, (s_w, s_h))
        p3 = cv2.resize(img_q90, (s_w, s_h))
        p_orig = cv2.resize(img_bgr, (s_w, s_h))
        cv2.putText(p_orig, "Original Uncompressed", (15, 30), font, 0.6, (255, 255, 255), 2)
        row1 = np.hstack([p_orig, p3])
        row2 = np.hstack([p2, p1])
        collage = np.vstack([row1, row2])
    else:
        collage = np.hstack([img_q90, img_q50, img_q10])
        
    metadata = {
        "q90_psnr_db": psnr_90,
        "q50_psnr_db": psnr_50,
        "q10_psnr_db": psnr_10,
        "dct_blockiness": "Noticeable 8x8 block boundary discontinuities visible in Q=10",
        "description": "Multi-tier JPEG DCT lossy compression comparison illustrating frequency quantization artifacts and rate-distortion trade-off."
    }
    return collage, metadata
