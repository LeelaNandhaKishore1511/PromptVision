import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional

def run_rotation(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    angle = float(params.get("angle", 30.0))
    h, w = img_bgr.shape[:2]
    center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img_bgr, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    metadata = {
        "transformation": "Planar 2D Euclidean Rotation",
        "angle_degrees": angle,
        "center_point": list(center),
        "transformation_matrix": M.tolist(),
        "description": f"Applied {angle}° counter-clockwise rotation about image center with reflection boundary extension."
    }
    return rotated, metadata

def run_translation(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    dx = float(params.get("dx", 50))
    dy = float(params.get("dy", 30))
    h, w = img_bgr.shape[:2]
    
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    translated = cv2.warpAffine(img_bgr, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(40, 40, 40))
    
    metadata = {
        "transformation": "Planar Translation (Shift)",
        "shift_x_px": dx,
        "shift_y_px": dy,
        "transformation_matrix": M.tolist(),
        "description": f"Shifted image plane by dx={dx}px, dy={dy}px with neutral border padding."
    }
    return translated, metadata

def run_scaling(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    scale_x = float(params.get("scale_x", 1.2))
    scale_y = float(params.get("scale_y", 1.2))
    h, w = img_bgr.shape[:2]
    
    new_w, new_h = int(w * scale_x), int(h * scale_y)
    scaled = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    
    # Crop or pad back to original canvas for consistent display
    canvas = np.zeros_like(img_bgr)
    insert_w = min(w, new_w)
    insert_h = min(h, new_h)
    canvas[:insert_h, :insert_w] = scaled[:insert_h, :insert_w]
    
    metadata = {
        "transformation": "Spatial Affine Scaling",
        "scale_factor_x": scale_x,
        "scale_factor_y": scale_y,
        "resampled_dimensions": f"{new_w}x{new_h}",
        "description": f"Bicubic interpolation scaling with scale_x={scale_x}, scale_y={scale_y}."
    }
    return canvas, metadata

def run_rigid_transformation(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Rigid Euclidean Transformation: Isometric Rotation + Translation (preserves distances and angles)."""
    angle = float(params.get("angle", 20.0))
    dx = float(params.get("dx", 40.0))
    dy = float(params.get("dy", -20.0))
    h, w = img_bgr.shape[:2]
    
    # Form 2x3 Euclidean matrix: [ [cos, -sin, dx], [sin, cos, dy] ]
    rad = np.radians(angle)
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    cx, cy = w / 2.0, h / 2.0
    
    # Rotate around center then translate
    tx = dx + (1 - cos_a)*cx + sin_a*cy
    ty = dy - sin_a*cx + (1 - cos_a)*cy
    M = np.array([[cos_a, -sin_a, tx], [sin_a, cos_a, ty]], dtype=np.float32)
    
    rigid_img = cv2.warpAffine(img_bgr, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    metadata = {
        "transformation": "Rigid Euclidean Isometry (SE(2))",
        "degrees_of_freedom": 3, # 1 rotation, 2 translations
        "angle_deg": angle,
        "translation_vector": [dx, dy],
        "isometry_preserved": "Distances, lengths, and angles strictly preserved",
        "description": f"Rigid Euclidean transformation (3 DOF: {angle}° rotation + [{dx}, {dy}] translation)."
    }
    return rigid_img, metadata

def run_affine_transformation(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """General 6-DOF Affine mapping using 3-point correspondence (shearing + scaling + rotation + translation)."""
    h, w = img_bgr.shape[:2]
    pts1 = np.float32([[50, 50], [w - 50, 50], [50, h - 50]])
    
    shear = float(params.get("shear", 0.2))
    pts2 = np.float32([[50 + shear*h*0.3, 50], [w - 30, 70], [30, h - 30]])
    
    M = cv2.getAffineTransform(pts1, pts2)
    affine_img = cv2.warpAffine(img_bgr, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    # Overlay deformed coordinate grid
    grid_img = affine_img.copy()
    for gx in range(0, w, 60):
        cv2.line(grid_img, (gx, 0), (gx, h), (0, 100, 255), 1)
    for gy in range(0, h, 60):
        cv2.line(grid_img, (0, gy), (w, gy), (0, 100, 255), 1)
    blended = cv2.addWeighted(affine_img, 0.7, grid_img, 0.3, 0)
    
    metadata = {
        "transformation": "General 6-DOF Affine Transformation",
        "degrees_of_freedom": 6,
        "shear_coefficient": shear,
        "parallelism_preserved": True,
        "affine_matrix": M.tolist(),
        "description": "6-parameter affine transform preserving collinearity, ratios of distances, and parallel lines."
    }
    return blended, metadata

def run_orb_alignment_registration(
    img_bgr: np.ndarray,
    params: Dict[str, Any],
    second_bgr: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Feature-based image registration aligning a moving image to reference image using ORB + RANSAC."""
    ref_img = img_bgr
    h, w = ref_img.shape[:2]
    
    if second_bgr is not None:
        moving_img = cv2.resize(second_bgr, (w, h))
        is_demo = False
    else:
        # Create synthetic misaligned moving image
        M_sim = cv2.getRotationMatrix2D((w//2, h//2), 12, 0.95)
        M_sim[0, 2] += 25
        M_sim[1, 2] -= 15
        moving_img = cv2.warpAffine(ref_img, M_sim, (w, h), borderMode=cv2.BORDER_REFLECT)
        is_demo = True
        
    orb = cv2.ORB_create(nfeatures=1000)
    kp_ref, des_ref = orb.detectAndCompute(ref_img, None)
    kp_mov, des_mov = orb.detectAndCompute(moving_img, None)
    
    if des_ref is None or des_mov is None or len(des_ref) < 8 or len(des_mov) < 8:
        return img_bgr, {"error": "Insufficient ORB features to compute registration homography"}
        
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des_mov, des_ref)
    matches = sorted(matches, key=lambda x: x.distance)[:100]
    
    pts_mov = np.float32([kp_mov[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts_ref = np.float32([kp_ref[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Estimate Homography using RANSAC
    H, mask = cv2.findHomography(pts_mov, pts_ref, cv2.RANSAC, 5.0)
    if H is None:
        return img_bgr, {"error": "RANSAC failed to find robust homography"}
        
    aligned_moving = cv2.warpPerspective(moving_img, H, (w, h))
    
    # Overlay registration checkerboard / blend (Green=Ref, Magenta=Registered Moving)
    blend = cv2.addWeighted(ref_img, 0.5, aligned_moving, 0.5, 0)
    
    inliers = int(np.sum(mask)) if mask is not None else len(matches)
    inlier_ratio = round((inliers / len(matches)) * 100, 1) if matches else 0
    
    metadata = {
        "algorithm": "Feature-Based Image Registration (ORB + RANSAC Homography)",
        "inlier_matches": inliers,
        "total_candidate_matches": len(matches),
        "ransac_inlier_ratio_pct": inlier_ratio,
        "homography_matrix": H.tolist(),
        "is_synthetic_pair": is_demo,
        "description": f"Registered moving image to reference plane using RANSAC projective homography ({inlier_ratio}% inlier consensus)."
    }
    return blend, metadata

def run_deformable_registration_demo(img_bgr: np.ndarray, params: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Simplified Deformable Registration demonstration using elastic displacement fields.
    Explicitly labeled: Simplified demonstration; NOT a medical-grade deformable registration system.
    """
    h, w = img_bgr.shape[:2]
    amplitude = float(params.get("amplitude", 15.0))
    
    # Generate smooth non-rigid displacement field
    x = np.linspace(0, 4*np.pi, w)
    y = np.linspace(0, 4*np.pi, h)
    xx, yy = np.meshgrid(x, y)
    
    dx = (np.sin(xx) * np.cos(yy) * amplitude).astype(np.float32)
    dy = (np.cos(xx) * np.sin(yy) * amplitude).astype(np.float32)
    
    grid_x, grid_y = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    map_x = grid_x + dx
    map_y = grid_y + dy
    
    deformed = cv2.remap(img_bgr, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    
    # Overlay vector field quiver representation
    overlay = deformed.copy()
    step = max(20, min(w, h) // 15)
    for gy in range(step//2, h, step):
        for gx in range(step//2, w, step):
            vx = int(dx[gy, gx] * 1.5)
            vy = int(dy[gy, gx] * 1.5)
            cv2.arrowedLine(overlay, (gx, gy), (gx + vx, gy + vy), (0, 255, 255), 1, tipLength=0.3)
            
    metadata = {
        "algorithm": "Simplified Deformable Registration (Elastic Displacement Field Demo)",
        "peak_displacement_px": amplitude,
        "grid_deformation_type": "B-spline / Harmonic Smooth Displacement Vector Field",
        "academic_notice": "Simplified educational demonstration of non-rigid displacement field modeling. Not intended or certified as a clinical medical-grade registration system.",
        "description": f"Modeled non-rigid elastic deformation field with vector quiver visualization ({amplitude}px peak deformation)."
    }
    return overlay, metadata

def run_optical_flow_farneback(
    img_bgr: np.ndarray,
    params: Dict[str, Any],
    second_bgr: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Computes dense optical flow using Gunnar Farneback's algorithm and visualizes as HSV motion wheel."""
    h, w = img_bgr.shape[:2]
    gray1 = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    if second_bgr is not None:
        work2 = cv2.resize(second_bgr, (w, h))
        gray2 = cv2.cvtColor(work2, cv2.COLOR_BGR2GRAY)
        is_synthetic = False
    else:
        # Create frame 2 with slight rotational translation
        M = cv2.getRotationMatrix2D((w//2, h//2), 2.5, 1.0)
        M[0, 2] += 6
        frame2 = cv2.warpAffine(img_bgr, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        is_synthetic = True
        
    flow = cv2.calcOpticalFlowFarneback(
        gray1, gray2, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    # HSV visualization: Hue = direction, Value = magnitude
    hsv = np.zeros_like(img_bgr)
    hsv[..., 1] = 255
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    flow_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    mean_speed = round(float(np.mean(mag)), 2)
    max_speed = round(float(np.max(mag)), 2)
    
    metadata = {
        "algorithm": "Gunnar Farneback Dense Optical Flow",
        "pyramid_scale": 0.5,
        "window_size": 15,
        "mean_motion_velocity_px": mean_speed,
        "max_motion_velocity_px": max_speed,
        "motion_representation": "HSV Color Wheel (Hue = Angle of motion, Saturation = 100%, Value = Velocity magnitude)",
        "synthetic_temporal_shift": is_synthetic,
        "description": f"Dense polynomial expansion optical flow field (Mean speed: {mean_speed}px/frame, Max speed: {max_speed}px/frame)."
    }
    return flow_rgb, metadata
