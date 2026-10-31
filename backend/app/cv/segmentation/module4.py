import cv2
import numpy as np
from typing import Dict, Any, Tuple
from skimage.segmentation import active_contour, felzenszwalb, slic, mark_boundaries
from skimage.color import rgb2gray
from skimage.filters import gaussian

def run_active_contours(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Active Contours (Snakes) energy-minimizing spline using scikit-image."""
    h, w = img_bgr.shape[:2]
    # Downsample if high resolution to keep latency low on CPU
    scale = 1.0
    if max(h, w) > 400:
        scale = 400.0 / max(h, w)
        work_img = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))
    else:
        work_img = img_bgr.copy()
        
    wh, ww = work_img.shape[:2]
    img_gray = cv2.cvtColor(work_img, cv2.COLOR_BGR2GRAY).astype(float) / 255.0
    smoothed = gaussian(img_gray, sigma=3.0)
    
    # Initialize snake as an ellipse centered in image
    s = np.linspace(0, 2*np.pi, 200)
    r = wh // 2 + (wh // 3) * np.sin(s)
    c = ww // 2 + (ww // 3) * np.cos(s)
    init_snake = np.array([r, c]).T
    
    alpha = float(params.get("alpha", 0.015)) # Elasticity
    beta = float(params.get("beta", 10.0))   # Rigidity
    gamma = float(params.get("gamma", 0.001)) # Step size
    
    snake = active_contour(smoothed, init_snake, alpha=alpha, beta=beta, gamma=gamma, max_num_iter=100)
    
    result = work_img.copy()
    # Draw initial snake in yellow
    for i in range(len(init_snake)):
        pt1 = (int(init_snake[i][1]), int(init_snake[i][0]))
        pt2 = (int(init_snake[(i+1)%len(init_snake)][1]), int(init_snake[(i+1)%len(init_snake)][0]))
        cv2.line(result, pt1, pt2, (0, 255, 255), 1)
        
    # Draw evolved snake in bright green
    for i in range(len(snake)):
        pt1 = (int(np.clip(snake[i][1], 0, ww-1)), int(np.clip(snake[i][0], 0, wh-1)))
        pt2 = (int(np.clip(snake[(i+1)%len(snake)][1], 0, ww-1)), int(np.clip(snake[(i+1)%len(snake)][0], 0, wh-1)))
        cv2.line(result, pt1, pt2, (0, 255, 0), 2)
        
    if scale != 1.0:
        result = cv2.resize(result, (w, h))
        
    metadata = {
        "algorithm": "Kass et al. Active Contours (Snake Model)",
        "snake_points": len(snake),
        "alpha_elasticity": alpha,
        "beta_rigidity": beta,
        "gamma_viscosity": gamma,
        "description": "Energy-minimizing spline driven by internal continuity/curvature forces and external image gradient attractors."
    }
    return result, metadata

def run_split_and_merge(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Quadtree recursive split-and-merge segmentation based on homogeneity criteria."""
    h, w = img_bgr.shape[:2]
    # Downsample for quadtree speed if needed
    scale = 1.0
    if max(h, w) > 300:
        scale = 300.0 / max(h, w)
        work_img = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))
    else:
        work_img = img_bgr.copy()
        
    gray = cv2.cvtColor(work_img, cv2.COLOR_BGR2GRAY)
    var_threshold = float(params.get("var_threshold", 25.0))
    min_size = int(params.get("min_size", 8))
    
    output = np.zeros_like(gray)
    quad_boxes = []
    
    def split(x, y, size):
        sub = gray[y:y+size, x:x+size]
        if sub.size == 0:
            return
        std_val = np.std(sub)
        if std_val > var_threshold and size > min_size:
            half = size // 2
            split(x, y, half)
            split(x + half, y, half)
            split(x, y + half, half)
            split(x + half, y + half, half)
        else:
            mean_val = int(np.mean(sub))
            output[y:y+size, x:x+size] = mean_val
            quad_boxes.append((x, y, size))
            
    # Process power-of-two blocks
    size = min(work_img.shape[0], work_img.shape[1])
    # nearest smaller power of 2
    pot = 1
    while pot * 2 <= size:
        pot *= 2
    split(0, 0, pot)
    
    # Overlay quadtree wireframe on color image
    color_seg = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    for (qx, qy, qs) in quad_boxes:
        cv2.rectangle(color_seg, (qx, qy), (qx+qs, qy+qs), (0, 180, 255), 1)
        
    if scale != 1.0:
        color_seg = cv2.resize(color_seg, (w, h), interpolation=cv2.INTER_NEAREST)
        
    metadata = {
        "algorithm": "Hierarchical Quadtree Split-and-Merge",
        "variance_threshold": var_threshold,
        "leaf_regions_count": len(quad_boxes),
        "minimum_quad_size": min_size,
        "description": f"Decomposed spatial domain into {len(quad_boxes)} homogeneous quadtree leaves based on intensity variance threshold."
    }
    return color_seg, metadata

def run_watershed(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Marker-based morphological watershed segmentation."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Noise removal with opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Finding sure foreground area with Euclidean distance transform
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    
    # Unknown boundary region
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is 1 not 0
    markers = markers + 1
    markers[unknown == 255] = 0
    
    result = img_bgr.copy()
    markers = cv2.watershed(result, markers)
    
    # Draw watershed dams in red
    result[markers == -1] = [0, 0, 255]
    
    # Create distinct colored segments
    num_labels = np.max(markers)
    color_mask = np.zeros_like(img_bgr)
    np.random.seed(42)
    colors = np.random.randint(50, 255, size=(max(2, num_labels + 1), 3), dtype=np.uint8)
    
    for l in range(2, num_labels + 1):
        color_mask[markers == l] = colors[l]
        
    blended = cv2.addWeighted(result, 0.6, color_mask, 0.4, 0)
    blended[markers == -1] = [0, 0, 255]
    
    metadata = {
        "algorithm": "Marker-Controlled Morphological Watershed",
        "identified_catchment_basins": int(num_labels - 1),
        "distance_transform_peak": round(float(dist_transform.max()), 1),
        "description": f"Flooded topological gradient relief map to partition into {num_labels - 1} catchment basins with watershed boundary ridges."
    }
    return blended, metadata

def run_mean_shift(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Mean Shift non-parametric clustering segmentation."""
    sp_radius = int(params.get("spatial_radius", 15))
    color_radius = int(params.get("color_radius", 25))
    
    h, w = img_bgr.shape[:2]
    scale = 1.0
    if max(h, w) > 500:
        scale = 500.0 / max(h, w)
        work_img = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))
    else:
        work_img = img_bgr.copy()
        
    shifted = cv2.pyrMeanShiftFiltering(work_img, sp_radius, color_radius, maxLevel=2)
    
    if scale != 1.0:
        shifted = cv2.resize(shifted, (w, h))
        
    # Count unique quantized colors as segment proxy
    unique_colors = len(np.unique(shifted.reshape(-1, 3), axis=0))
    
    metadata = {
        "algorithm": "Mean Shift Mode Seeking Segmentation",
        "spatial_radius": sp_radius,
        "color_space_radius": color_radius,
        "quantized_color_modes": unique_colors,
        "description": "Non-parametric kernel density estimation clustering pixels towards local modal density centers in joint spatial-range space."
    }
    return shifted, metadata

def run_graph_segmentation(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Felzenszwalb's efficient graph-based image segmentation."""
    h, w = img_bgr.shape[:2]
    scale = 1.0
    if max(h, w) > 400:
        scale = 400.0 / max(h, w)
        work_img = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))
    else:
        work_img = img_bgr.copy()
        
    img_rgb = cv2.cvtColor(work_img, cv2.COLOR_BGR2RGB)
    scale_param = float(params.get("scale", 100))
    sigma = float(params.get("sigma", 0.8))
    min_size = int(params.get("min_size", 50))
    
    segments = felzenszwalb(img_rgb, scale=scale_param, sigma=sigma, min_size=min_size)
    num_segments = len(np.unique(segments))
    
    # Create colored visualization
    np.random.seed(123)
    palette = np.random.randint(0, 255, size=(num_segments, 3), dtype=np.uint8)
    
    # Map segment indices to 0..num_segments-1
    _, inverse = np.unique(segments, return_inverse=True)
    seg_color = palette[inverse].reshape(work_img.shape)
    
    # Boundaries
    boundaries = mark_boundaries(work_img, segments, color=(1, 1, 0))
    bound_bgr = (boundaries * 255).astype(np.uint8)
    
    if scale != 1.0:
        bound_bgr = cv2.resize(bound_bgr, (w, h))
        
    metadata = {
        "algorithm": "Felzenszwalb-Huttenlocher Graph-Based Segmentation",
        "graph_scale_parameter": scale_param,
        "gaussian_sigma": sigma,
        "minimum_component_size": min_size,
        "total_graph_components": num_segments,
        "description": f"Kruskal-style minimum spanning tree graph clustering partitioned image into {num_segments} perceptually uniform regions."
    }
    return bound_bgr, metadata

def run_superpixels_slic(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """SLIC Superpixels (Normalized Cut / Spectral Clustering proxy representation)."""
    h, w = img_bgr.shape[:2]
    scale = 1.0
    if max(h, w) > 450:
        scale = 450.0 / max(h, w)
        work_img = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))
    else:
        work_img = img_bgr.copy()
        
    img_rgb = cv2.cvtColor(work_img, cv2.COLOR_BGR2RGB)
    n_segments = int(params.get("n_segments", 100))
    compactness = float(params.get("compactness", 10.0))
    
    segments = slic(img_rgb, n_segments=n_segments, compactness=compactness, start_label=1)
    actual_segments = len(np.unique(segments))
    
    bounded = mark_boundaries(work_img, segments, color=(0, 1, 0))
    res_bgr = (bounded * 255).astype(np.uint8)
    
    if scale != 1.0:
        res_bgr = cv2.resize(res_bgr, (w, h))
        
    metadata = {
        "algorithm": "SLIC Superpixel (Normalized Cut Graph Proxy)",
        "requested_superpixels": n_segments,
        "actual_superpixels_formed": actual_segments,
        "compactness_parameter": compactness,
        "description": f"Formed {actual_segments} compact superpixels in 5D CIELAB-spatial space, reducing computational graph complexity for normalized cuts."
    }
    return res_bgr, metadata
