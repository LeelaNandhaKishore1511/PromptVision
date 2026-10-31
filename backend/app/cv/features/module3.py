import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional

def run_template_matching(
    img_bgr: np.ndarray,
    params: Dict[str, Any],
    template_bgr: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Performs normalized cross-correlation template matching."""
    h_img, w_img = img_bgr.shape[:2]
    result_img = img_bgr.copy()
    
    # If no second template provided, extract a central region of interest as a demonstration template
    if template_bgr is None:
        th, tw = min(60, h_img // 4), min(60, w_img // 4)
        cy, cx = h_img // 2, w_img // 2
        template = img_bgr[cy - th//2 : cy + th//2, cx - tw//2 : cx + tw//2]
        is_demo_template = True
    else:
        template = template_bgr
        is_demo_template = False
        
    th, tw = template.shape[:2]
    if th >= h_img or tw >= w_img:
        # Resize template to fit inside target
        scale = min((h_img * 0.5) / th, (w_img * 0.5) / tw)
        template = cv2.resize(template, (max(10, int(tw * scale)), max(10, int(th * scale))))
        th, tw = template.shape[:2]
        
    res = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    top_left = max_loc
    bottom_right = (top_left[0] + tw, top_left[1] + th)
    cv2.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 3)
    cv2.putText(
        result_img,
        f"Match: {round(max_val, 2)}",
        (top_left[0], max(20, top_left[1] - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )
    
    metadata = {
        "template_size": f"{tw}x{th}",
        "peak_correlation_score": round(float(max_val), 3),
        "best_match_top_left": list(top_left),
        "is_auto_extracted_patch": is_demo_template,
        "description": f"Template matching via TM_CCOEFF_NORMED. Peak normalized correlation: {round(max_val, 3)}."
    }
    return result_img, metadata

def run_harris_corners(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    block_size = int(params.get("block_size", 2))
    ksize = int(params.get("ksize", 3))
    k = float(params.get("k", 0.04))
    
    dst = cv2.cornerHarris(gray, block_size, ksize, k)
    # Dilate corner markings for clearer visualization
    dst_dilated = cv2.dilate(dst, None)
    
    result = img_bgr.copy()
    threshold = 0.01 * dst.max()
    corner_mask = dst_dilated > threshold
    result[corner_mask] = [0, 0, 255] # Mark corners in bright red
    
    corner_count = int(np.count_nonzero(corner_mask))
    
    metadata = {
        "algorithm": "Harris Corner Detection",
        "detected_corners_count": corner_count,
        "block_size": block_size,
        "sobel_aperture": ksize,
        "harris_free_parameter_k": k,
        "description": f"Identified {corner_count} structural corner keypoints using auto-correlation matrix eigenvalue response."
    }
    return result, metadata

def run_sobel_edges(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    ksize = int(params.get("ksize", 3))
    if ksize not in [1, 3, 5, 7]:
        ksize = 3
        
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    
    mag = np.sqrt(sobel_x**2 + sobel_y**2)
    norm_mag = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    colored_edges = cv2.applyColorMap(norm_mag, cv2.COLORMAP_TURBO)
    
    metadata = {
        "algorithm": "Sobel Gradient Operator",
        "kernel_size": f"{ksize}x{ksize}",
        "mean_gradient_magnitude": round(float(np.mean(mag)), 2),
        "max_gradient_magnitude": round(float(np.max(mag)), 2),
        "description": "Computed first-order directional derivatives along X and Y axes to produce continuous edge gradient vector magnitude."
    }
    return colored_edges, metadata

def run_canny_edges(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    low_thresh = int(params.get("low_threshold", 50))
    high_thresh = int(params.get("high_threshold", 150))
    
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, low_thresh, high_thresh)
    
    edge_pixels = int(np.count_nonzero(edges))
    edge_density = round((edge_pixels / edges.size) * 100, 2)
    
    # Overlay edges on original image in cyan
    overlay = img_bgr.copy()
    overlay[edges > 0] = [255, 255, 0] # Cyan edges
    
    metadata = {
        "algorithm": "Canny Multi-Stage Edge Detector",
        "hysteresis_low_threshold": low_thresh,
        "hysteresis_high_threshold": high_thresh,
        "total_edge_pixels": edge_pixels,
        "edge_density_pct": edge_density,
        "description": f"Multi-stage edge detection (Gaussian filter, Sobel gradient, Non-Maximum Suppression, Hysteresis thresholding). Edge density: {edge_density}%."
    }
    return overlay, metadata

def run_laplacian_edges(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    variance = float(lap.var()) # Standard measure of sharpness/focus
    
    norm_lap = cv2.normalize(np.abs(lap), None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    lap_bgr = cv2.cvtColor(norm_lap, cv2.COLOR_GRAY2BGR)
    
    focus_label = "Sharp / In-Focus" if variance > 100 else ("Moderate Focus" if variance > 30 else "Blurry / Soft")
    
    metadata = {
        "algorithm": "Laplacian Second-Order Differential Operator",
        "laplacian_variance_focus_measure": round(variance, 2),
        "focus_quality_estimate": focus_label,
        "description": f"Second-derivative isotropic Laplacian operator revealing zero-crossings. Image focus sharpness variance: {round(variance, 2)} ({focus_label})."
    }
    return lap_bgr, metadata

def run_grid_detection(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Detects line structures and intersections using Probabilistic Hough Lines."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=40, maxLineGap=10)
    result = img_bgr.copy()
    
    line_count = 0
    if lines is not None:
        line_count = len(lines)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
    metadata = {
        "algorithm": "Probabilistic Hough Line Transform (Grid/Line Detector)",
        "detected_structural_lines": line_count,
        "grid_structure_present": line_count >= 10,
        "description": f"Identified {line_count} rectilinear line segments and structural axes using parametric Hough voting accumulator."
    }
    return result, metadata

def run_contour_extraction(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = img_bgr.copy()
    
    valid_contours = [c for c in contours if cv2.contourArea(c) > 20]
    cv2.drawContours(result, valid_contours, -1, (0, 255, 0), 2)
    
    # Calculate areas
    areas = [cv2.contourArea(c) for c in valid_contours]
    total_contour_area = sum(areas)
    max_area = max(areas) if areas else 0
    
    metadata = {
        "algorithm": "Topological Contour Extraction",
        "total_contours_found": len(valid_contours),
        "largest_contour_area_px": round(float(max_area), 1),
        "total_contour_area_px": round(float(total_contour_area), 1),
        "description": f"Extracted {len(valid_contours)} closed boundary contours using topological border following algorithm."
    }
    return result, metadata

def run_bounding_boxes(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result = img_bgr.copy()
    boxes = []
    # Sort by area descending and take top 15
    sorted_cnts = sorted([c for c in contours if cv2.contourArea(c) > 50], key=cv2.contourArea, reverse=True)[:15]
    
    for i, c in enumerate(sorted_cnts):
        x, y, w, h = cv2.boundingRect(c)
        boxes.append({"id": i+1, "x": x, "y": y, "width": w, "height": h, "area": w*h})
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 100, 0), 2)
        cv2.putText(result, f"#{i+1}", (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 1)
        
    metadata = {
        "algorithm": "Salient Region Bounding Box Extraction",
        "extracted_bounding_boxes": len(boxes),
        "box_coordinates": boxes[:5], # First 5 for brevity
        "description": f"Extracted {len(boxes)} bounding boxes enclosing dominant foreground components."
    }
    return result, metadata

def run_orb_features(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    n_features = int(params.get("n_features", 500))
    orb = cv2.ORB_create(nfeatures=n_features)
    
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    # Draw keypoints with size and orientation vectors
    result = cv2.drawKeypoints(
        img_bgr,
        keypoints,
        None,
        color=(0, 255, 128),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    metadata = {
        "algorithm": "ORB (Oriented FAST and Rotated BRIEF)",
        "keypoints_detected": len(keypoints),
        "descriptor_dimension": descriptors.shape[1] if descriptors is not None else 0,
        "scale_rotation_invariant": True,
        "description": f"Detected {len(keypoints)} scale- and rotation-invariant keypoints with oriented BRIEF descriptors."
    }
    return result, metadata

def run_orb_matching(
    img_bgr: np.ndarray,
    params: Dict[str, Any],
    second_bgr: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Matches ORB feature descriptors between two images or against a rotated version."""
    orb = cv2.ORB_create(nfeatures=500)
    
    img1 = img_bgr
    if second_bgr is not None:
        img2 = second_bgr
        is_second_upload = True
    else:
        # Generate slightly rotated/scaled test pair
        h, w = img_bgr.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), 15, 0.9)
        img2 = cv2.warpAffine(img_bgr, M, (w, h))
        is_second_upload = False
        
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    
    if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
        return img_bgr, {"error": "Insufficient descriptors for ORB matching"}
        
    # Match using Hamming distance (suitable for binary descriptors)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    top_matches = matches[:40]
    matched_img = cv2.drawMatches(
        img1, kp1, img2, kp2, top_matches, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    metadata = {
        "algorithm": "ORB Feature Matching (Brute-Force Hamming Distance)",
        "total_matches_found": len(matches),
        "top_matches_visualized": len(top_matches),
        "average_top_match_distance": round(float(np.mean([m.distance for m in top_matches])), 2) if top_matches else 0,
        "matched_against_second_upload": is_second_upload,
        "description": f"Matched {len(matches)} corresponding feature pairs using Hamming distance across scale/rotation changes."
    }
    return matched_img, metadata

def run_haar_faces(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Haar Cascade Face Detection.
    Explicitly labeled: Does NOT perform biometric identity recognition.
    """
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    scale_factor = float(params.get("scale_factor", 1.1))
    min_neighbors = int(params.get("min_neighbors", 5))
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=(30, 30))
    result = img_bgr.copy()
    
    detected_boxes = []
    for (x, y, w, h) in faces:
        detected_boxes.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(result, "Face Region (Object Detection)", (x, max(20, y-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
    metadata = {
        "algorithm": "Viola-Jones Haar Cascade Classifier (Frontal Face)",
        "detected_faces_count": len(faces),
        "face_bounding_boxes": detected_boxes,
        "privacy_and_capability_notice": "Haar cascade detects human face structures (eyes, nose bridge, cheeks geometry). It does NOT perform facial identification or identity recognition.",
        "description": f"Detected {len(faces)} face bounding regions using AdaBoost Haar-like rectangular feature cascades."
    }
    return result, metadata

def run_haar_eyes(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Haar Cascade Eye Detection."""
    cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
    eye_cascade = cv2.CascadeClassifier(cascade_path)
    
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))
    result = img_bgr.copy()
    
    for (x, y, w, h) in eyes:
        cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(result, "Eye", (x, max(15, y-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
        
    metadata = {
        "algorithm": "Haar Cascade Eye Detector",
        "detected_eyes_count": len(eyes),
        "description": f"Detected {len(eyes)} ocular feature regions via Haar eye cascade classifier."
    }
    return result, metadata
