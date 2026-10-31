import time
import uuid
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from ..config import UPLOADS_DIR, PROCESSED_DIR
from .introduction import module1
from .filtering import module2
from .features import module3
from .segmentation import module4
from .transformations import module5

# Unified CV Catalog
CV_CATALOG = {
    "module1": {
        "id": "module1",
        "title": "Module 1: Introduction to Computer Vision",
        "syllabus": "Image formation, representations, sampling theorem, frequency domain, wavelets",
        "operations": [
            {
                "id": "rgb_grayscale",
                "name": "RGB & Grayscale Channels Representation",
                "description": "Visualizes color channel decomposition (R, G, B heatmaps) and luminance conversion.",
                "parameters": []
            },
            {
                "id": "pixel_inspection",
                "name": "Pixel Intensity & Shannon Entropy Inspection",
                "description": "Calculates pixel intensity distribution, statistics, and Shannon information entropy.",
                "parameters": []
            },
            {
                "id": "sampling_demo",
                "name": "Nyquist-Shannon Sampling & Aliasing Demonstration",
                "description": "Demonstrates downsampling aliasing vs Gaussian anti-aliased reconstruction.",
                "parameters": [
                    {"name": "factor", "label": "Downsampling Factor", "type": "select", "options": [2, 4, 8, 16], "default": 4}
                ]
            },
            {
                "id": "fourier_transform",
                "name": "2D Fast Fourier Transform (FFT) Spectrum",
                "description": "Computes 2D FFT log magnitude spectrum showing spatial frequency distribution.",
                "parameters": []
            },
            {
                "id": "wavelet_decomposition",
                "name": "2D Haar Wavelet Decomposition (LL, LH, HL, HH)",
                "description": "Decomposes image into multi-resolution approximation and detail subbands.",
                "parameters": []
            }
        ]
    },
    "module2": {
        "id": "module2",
        "title": "Module 2: Image Filtering & Enhancement",
        "syllabus": "Filtering, thresholding, morphological operators, histogram equalization, compression",
        "operations": [
            {
                "id": "averaging_filter",
                "name": "Averaging (Box) Spatial Filter",
                "description": "Uniform spatial low-pass filter for high-frequency noise attenuation.",
                "parameters": [
                    {"name": "kernel_size", "label": "Kernel Size (Odd)", "type": "slider", "min": 3, "max": 25, "step": 2, "default": 7}
                ]
            },
            {
                "id": "gaussian_filter",
                "name": "Gaussian Smoothing Filter",
                "description": "2D Gaussian weighted low-pass filter for isotropic noise reduction.",
                "parameters": [
                    {"name": "kernel_size", "label": "Kernel Size", "type": "slider", "min": 3, "max": 25, "step": 2, "default": 7},
                    {"name": "sigma", "label": "Sigma (Standard Deviation)", "type": "slider", "min": 0.5, "max": 5.0, "step": 0.5, "default": 1.5}
                ]
            },
            {
                "id": "median_filter",
                "name": "Median Non-Linear Filter",
                "description": "Order-statistic filter for salt-and-pepper noise removal while preserving sharp edges.",
                "parameters": [
                    {"name": "kernel_size", "label": "Kernel Size (Odd)", "type": "slider", "min": 3, "max": 15, "step": 2, "default": 5}
                ]
            },
            {
                "id": "bilateral_filter",
                "name": "Bilateral Edge-Preserving Filter",
                "description": "Non-linear filter combining spatial distance and radiometric intensity difference.",
                "parameters": [
                    {"name": "diameter", "label": "Pixel Diameter", "type": "slider", "min": 3, "max": 15, "step": 2, "default": 9},
                    {"name": "sigma_color", "label": "Sigma Color", "type": "slider", "min": 20, "max": 150, "step": 5, "default": 75},
                    {"name": "sigma_space", "label": "Sigma Space", "type": "slider", "min": 20, "max": 150, "step": 5, "default": 75}
                ]
            },
            {
                "id": "thresholding",
                "name": "Image Thresholding (Otsu / Binary / Adaptive)",
                "description": "Binarizes image using global, adaptive, or Otsu's variance-minimizing threshold.",
                "parameters": [
                    {"name": "mode", "label": "Thresholding Method", "type": "select", "options": ["otsu", "binary", "adaptive_mean", "adaptive_gaussian"], "default": "otsu"},
                    {"name": "cutoff", "label": "Binary Cutoff Value", "type": "slider", "min": 0, "max": 255, "step": 1, "default": 127}
                ]
            },
            {
                "id": "morphological_ops",
                "name": "Morphological Operators (Erosion / Dilation / Open / Close)",
                "description": "Non-linear shape operations using structuring elements.",
                "parameters": [
                    {"name": "operation", "label": "Operation", "type": "select", "options": ["opening", "closing", "erosion", "dilation"], "default": "opening"},
                    {"name": "kernel_size", "label": "Structuring Element Size", "type": "slider", "min": 3, "max": 15, "step": 2, "default": 5},
                    {"name": "iterations", "label": "Iterations", "type": "slider", "min": 1, "max": 5, "step": 1, "default": 1}
                ]
            },
            {
                "id": "histogram_equalization",
                "name": "Histogram Equalization (Global / CLAHE)",
                "description": "Stretches dynamic range and contrast across cumulative distribution function.",
                "parameters": [
                    {"name": "method", "label": "Method", "type": "select", "options": ["clahe", "global"], "default": "clahe"},
                    {"name": "clip_limit", "label": "CLAHE Clip Limit", "type": "slider", "min": 1.0, "max": 5.0, "step": 0.5, "default": 2.5}
                ]
            },
            {
                "id": "jpeg_compression",
                "name": "JPEG DCT Quantization & Compression Analysis",
                "description": "Multi-tier JPEG DCT lossy compression comparison (Q=10, 50, 90) with PSNR.",
                "parameters": []
            }
        ]
    },
    "module3": {
        "id": "module3",
        "title": "Module 3: Feature Detection & Matching",
        "syllabus": "Template matching, corners, edges, grids, contours, ORB features, Haar cascades",
        "operations": [
            {
                "id": "template_matching",
                "name": "Normalized Cross-Correlation Template Matching",
                "description": "Locates best matching spatial patch via TM_CCOEFF_NORMED.",
                "parameters": []
            },
            {
                "id": "harris_corners",
                "name": "Harris Corner Detection",
                "description": "Detects structural corner keypoints using auto-correlation eigenvalues.",
                "parameters": [
                    {"name": "block_size", "label": "Neighborhood Size", "type": "slider", "min": 2, "max": 6, "step": 1, "default": 2},
                    {"name": "k", "label": "Harris Detector Free Parameter k", "type": "slider", "min": 0.02, "max": 0.08, "step": 0.01, "default": 0.04}
                ]
            },
            {
                "id": "sobel_edges",
                "name": "Sobel Gradient Vector Magnitude",
                "description": "Computes first directional derivatives and continuous gradient magnitude.",
                "parameters": [
                    {"name": "ksize", "label": "Sobel Kernel Size", "type": "select", "options": [1, 3, 5, 7], "default": 3}
                ]
            },
            {
                "id": "canny_edges",
                "name": "Canny Multi-Stage Edge Detection",
                "description": "Multi-stage edge detection with Non-Maximum Suppression and hysteresis thresholding.",
                "parameters": [
                    {"name": "low_threshold", "label": "Low Hysteresis Threshold", "type": "slider", "min": 10, "max": 150, "step": 5, "default": 50},
                    {"name": "high_threshold", "label": "High Hysteresis Threshold", "type": "slider", "min": 50, "max": 250, "step": 5, "default": 150}
                ]
            },
            {
                "id": "laplacian_edges",
                "name": "Laplacian Operator & Image Sharpness Variance",
                "description": "Second-order isotropic derivative measuring zero-crossings and focus sharpness.",
                "parameters": []
            },
            {
                "id": "grid_detection",
                "name": "Grid and Structural Line Detection (Hough Lines)",
                "description": "Detects rectilinear structural grid axes and intersection points.",
                "parameters": []
            },
            {
                "id": "contour_extraction",
                "name": "Topological Contour Extraction & Geometric Properties",
                "description": "Extracts closed boundary contours, area, and perimeter.",
                "parameters": []
            },
            {
                "id": "bounding_boxes",
                "name": "Salient Object Bounding Box Extraction",
                "description": "Extracts bounding rectangles enclosing dominant foreground visual entities.",
                "parameters": []
            },
            {
                "id": "orb_features",
                "name": "ORB Feature Keypoints & Orientations",
                "description": "Extracts fast, rotation- and scale-invariant keypoints with oriented descriptors.",
                "parameters": [
                    {"name": "n_features", "label": "Max Keypoints", "type": "slider", "min": 100, "max": 1000, "step": 50, "default": 500}
                ]
            },
            {
                "id": "orb_matching",
                "name": "ORB Descriptor Feature Matching",
                "description": "Matches ORB binary descriptors across image pairs using Hamming distance.",
                "parameters": []
            },
            {
                "id": "haar_faces",
                "name": "Haar Cascade Frontal Face Detection",
                "description": "AdaBoost rectangular feature cascade for face bounding region detection.",
                "parameters": [
                    {"name": "scale_factor", "label": "Pyramid Scale Factor", "type": "slider", "min": 1.05, "max": 1.3, "step": 0.05, "default": 1.1},
                    {"name": "min_neighbors", "label": "Min Neighbor Rectangles", "type": "slider", "min": 3, "max": 8, "step": 1, "default": 5}
                ]
            },
            {
                "id": "haar_eyes",
                "name": "Haar Cascade Eye Feature Detection",
                "description": "Detects ocular feature regions via Haar cascade classifier.",
                "parameters": []
            }
        ]
    },
    "module4": {
        "id": "module4",
        "title": "Module 4: Image Segmentation",
        "syllabus": "Active contours, split and merge, watershed, Mean Shift, graph-based segmentation, superpixels",
        "operations": [
            {
                "id": "active_contours",
                "name": "Active Contours (Snake Model)",
                "description": "Energy-minimizing spline attracted to high image gradients.",
                "parameters": [
                    {"name": "alpha", "label": "Elasticity (Alpha)", "type": "slider", "min": 0.005, "max": 0.05, "step": 0.005, "default": 0.015},
                    {"name": "beta", "label": "Rigidity (Beta)", "type": "slider", "min": 1.0, "max": 20.0, "step": 1.0, "default": 10.0}
                ]
            },
            {
                "id": "split_and_merge",
                "name": "Hierarchical Quadtree Split-and-Merge",
                "description": "Recursive spatial quadtree decomposition based on intensity homogeneity.",
                "parameters": [
                    {"name": "var_threshold", "label": "Standard Deviation Threshold", "type": "slider", "min": 10.0, "max": 50.0, "step": 5.0, "default": 25.0}
                ]
            },
            {
                "id": "watershed",
                "name": "Marker-Controlled Morphological Watershed",
                "description": "Flooding of gradient relief map to partition touching or overlapping regions.",
                "parameters": []
            },
            {
                "id": "mean_shift",
                "name": "Mean Shift Clustering Segmentation",
                "description": "Non-parametric density estimation clustering pixels in joint spatial-color space.",
                "parameters": [
                    {"name": "spatial_radius", "label": "Spatial Window Radius", "type": "slider", "min": 5, "max": 30, "step": 5, "default": 15},
                    {"name": "color_radius", "label": "Color Distance Radius", "type": "slider", "min": 10, "max": 50, "step": 5, "default": 25}
                ]
            },
            {
                "id": "graph_segmentation",
                "name": "Felzenszwalb's Graph-Based Segmentation",
                "description": "Kruskal-style minimum spanning tree graph clustering into perceptually uniform components.",
                "parameters": [
                    {"name": "scale", "label": "Graph Scale Parameter", "type": "slider", "min": 50, "max": 300, "step": 25, "default": 100},
                    {"name": "min_size", "label": "Minimum Component Size", "type": "slider", "min": 20, "max": 150, "step": 10, "default": 50}
                ]
            },
            {
                "id": "superpixels_slic",
                "name": "SLIC Superpixels (Normalized Cut Graph Proxy)",
                "description": "Partitions image into compact, boundary-adherent superpixel clusters.",
                "parameters": [
                    {"name": "n_segments", "label": "Number of Superpixels", "type": "slider", "min": 30, "max": 200, "step": 10, "default": 80},
                    {"name": "compactness", "label": "Compactness Weight", "type": "slider", "min": 5.0, "max": 30.0, "step": 5.0, "default": 10.0}
                ]
            }
        ]
    },
    "module5": {
        "id": "module5",
        "title": "Module 5: Transformation, Alignment & Motion",
        "syllabus": "Rigid transforms, affine transforms, image registration, optical flow",
        "operations": [
            {
                "id": "rotation",
                "name": "2D Planar Rotation",
                "description": "Rotates image around center by specified angle.",
                "parameters": [
                    {"name": "angle", "label": "Rotation Angle (°)", "type": "slider", "min": -180, "max": 180, "step": 5, "default": 30}
                ]
            },
            {
                "id": "translation",
                "name": "Planar Translation (Shift)",
                "description": "Translates image plane along horizontal (dx) and vertical (dy) axes.",
                "parameters": [
                    {"name": "dx", "label": "Shift X (pixels)", "type": "slider", "min": -100, "max": 100, "step": 10, "default": 40},
                    {"name": "dy", "label": "Shift Y (pixels)", "type": "slider", "min": -100, "max": 100, "step": 10, "default": 20}
                ]
            },
            {
                "id": "scaling",
                "name": "Affine Spatial Rescaling",
                "description": "Isotropic and anisotropic scaling using bicubic interpolation.",
                "parameters": [
                    {"name": "scale_x", "label": "Scale X", "type": "slider", "min": 0.5, "max": 2.0, "step": 0.1, "default": 1.2},
                    {"name": "scale_y", "label": "Scale Y", "type": "slider", "min": 0.5, "max": 2.0, "step": 0.1, "default": 1.2}
                ]
            },
            {
                "id": "rigid_transformation",
                "name": "Rigid Euclidean Isometry (SE(2))",
                "description": "Combines rotation and translation while strictly preserving geometric distances.",
                "parameters": [
                    {"name": "angle", "label": "Angle (°)", "type": "slider", "min": -90, "max": 90, "step": 5, "default": 20},
                    {"name": "dx", "label": "Translate X", "type": "slider", "min": -80, "max": 80, "step": 10, "default": 30},
                    {"name": "dy", "label": "Translate Y", "type": "slider", "min": -80, "max": 80, "step": 10, "default": -20}
                ]
            },
            {
                "id": "affine_transformation",
                "name": "General 6-DOF Affine Transformation & Shear",
                "description": "Transforms image coordinates via 3-point affine mapping preserving parallelism.",
                "parameters": [
                    {"name": "shear", "label": "Shear Coefficient", "type": "slider", "min": -0.5, "max": 0.5, "step": 0.05, "default": 0.2}
                ]
            },
            {
                "id": "orb_registration",
                "name": "Feature-Based Image Registration (ORB + RANSAC)",
                "description": "Aligns moving image to reference image using projective homography.",
                "parameters": []
            },
            {
                "id": "deformable_registration",
                "name": "Simplified Deformable Registration (Elastic Displacement Field)",
                "description": "Simulates non-rigid elastic deformation vector field.",
                "parameters": [
                    {"name": "amplitude", "label": "Deformation Amplitude", "type": "slider", "min": 5.0, "max": 30.0, "step": 2.5, "default": 15.0}
                ]
            },
            {
                "id": "optical_flow",
                "name": "Gunnar Farneback Dense Optical Flow",
                "description": "Computes motion velocity field rendered as an HSV motion color wheel.",
                "parameters": []
            }
        ]
    }
}

class CVService:
    def get_catalog(self) -> Dict[str, Any]:
        return CV_CATALOG

    def _resolve_image_path(self, image_id: str) -> Optional[Path]:
        for ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
            p = UPLOADS_DIR / f"{image_id}{ext}"
            if p.exists():
                return p
        return None

    def execute_operation(
        self,
        op_id: str,
        img_bgr: np.ndarray,
        params: Dict[str, Any],
        second_bgr: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, Dict[str, Any], str, str]:
        """Dispatch operation to the corresponding module function."""
        # Module 1
        if op_id == "rgb_grayscale":
            res_img, meta = module1.run_rgb_grayscale(img_bgr, params)
            return res_img, meta, "RGB & Grayscale Representation", "Module 1"
        elif op_id == "pixel_inspection":
            res_img, meta = module1.run_pixel_inspection(img_bgr, params)
            return res_img, meta, "Pixel Intensity & Entropy", "Module 1"
        elif op_id == "sampling_demo":
            res_img, meta = module1.run_sampling_demonstration(img_bgr, params)
            return res_img, meta, "Nyquist-Shannon Sampling Demo", "Module 1"
        elif op_id == "fourier_transform":
            res_img, meta = module1.run_fourier_transform(img_bgr, params)
            return res_img, meta, "2D Fourier Transform Spectrum", "Module 1"
        elif op_id == "wavelet_decomposition":
            res_img, meta = module1.run_wavelet_decomposition(img_bgr, params)
            return res_img, meta, "2D Haar Wavelet Decomposition", "Module 1"

        # Module 2
        elif op_id == "averaging_filter":
            res_img, meta = module2.run_averaging_filter(img_bgr, params)
            return res_img, meta, "Averaging Box Filter", "Module 2"
        elif op_id == "gaussian_filter":
            res_img, meta = module2.run_gaussian_filter(img_bgr, params)
            return res_img, meta, "Gaussian Smoothing Filter", "Module 2"
        elif op_id == "median_filter":
            res_img, meta = module2.run_median_filter(img_bgr, params)
            return res_img, meta, "Median Non-Linear Filter", "Module 2"
        elif op_id == "bilateral_filter":
            res_img, meta = module2.run_bilateral_filter(img_bgr, params)
            return res_img, meta, "Bilateral Filter", "Module 2"
        elif op_id == "thresholding":
            res_img, meta = module2.run_thresholding(img_bgr, params)
            return res_img, meta, "Thresholding Binarization", "Module 2"
        elif op_id == "morphological_ops":
            res_img, meta = module2.run_morphological_ops(img_bgr, params)
            return res_img, meta, "Morphological Operators", "Module 2"
        elif op_id == "histogram_equalization":
            res_img, meta = module2.run_histogram_equalization(img_bgr, params)
            return res_img, meta, "Histogram Equalization / CLAHE", "Module 2"
        elif op_id == "jpeg_compression":
            res_img, meta = module2.run_jpeg_compression_comparison(img_bgr, params)
            return res_img, meta, "JPEG Compression & PSNR Analysis", "Module 2"

        # Module 3
        elif op_id == "template_matching":
            res_img, meta = module3.run_template_matching(img_bgr, params, second_bgr)
            return res_img, meta, "Template Matching (NCC)", "Module 3"
        elif op_id == "harris_corners":
            res_img, meta = module3.run_harris_corners(img_bgr, params)
            return res_img, meta, "Harris Corner Detection", "Module 3"
        elif op_id == "sobel_edges":
            res_img, meta = module3.run_sobel_edges(img_bgr, params)
            return res_img, meta, "Sobel Gradient Vector Magnitude", "Module 3"
        elif op_id == "canny_edges":
            res_img, meta = module3.run_canny_edges(img_bgr, params)
            return res_img, meta, "Canny Edge Detection", "Module 3"
        elif op_id == "laplacian_edges":
            res_img, meta = module3.run_laplacian_edges(img_bgr, params)
            return res_img, meta, "Laplacian & Focus Variance", "Module 3"
        elif op_id == "grid_detection":
            res_img, meta = module3.run_grid_detection(img_bgr, params)
            return res_img, meta, "Grid & Line Detection (Hough)", "Module 3"
        elif op_id == "contour_extraction":
            res_img, meta = module3.run_contour_extraction(img_bgr, params)
            return res_img, meta, "Contour Extraction", "Module 3"
        elif op_id == "bounding_boxes":
            res_img, meta = module3.run_bounding_boxes(img_bgr, params)
            return res_img, meta, "Salient Region Bounding Boxes", "Module 3"
        elif op_id == "orb_features":
            res_img, meta = module3.run_orb_features(img_bgr, params)
            return res_img, meta, "ORB Keypoint Detection", "Module 3"
        elif op_id == "orb_matching":
            res_img, meta = module3.run_orb_matching(img_bgr, params, second_bgr)
            return res_img, meta, "ORB Feature Matching", "Module 3"
        elif op_id == "haar_faces":
            res_img, meta = module3.run_haar_faces(img_bgr, params)
            return res_img, meta, "Haar Cascade Face Detection", "Module 3"
        elif op_id == "haar_eyes":
            res_img, meta = module3.run_haar_eyes(img_bgr, params)
            return res_img, meta, "Haar Cascade Eye Detection", "Module 3"

        # Module 4
        elif op_id == "active_contours":
            res_img, meta = module4.run_active_contours(img_bgr, params)
            return res_img, meta, "Active Contours (Snakes)", "Module 4"
        elif op_id == "split_and_merge":
            res_img, meta = module4.run_split_and_merge(img_bgr, params)
            return res_img, meta, "Quadtree Split-and-Merge", "Module 4"
        elif op_id == "watershed":
            res_img, meta = module4.run_watershed(img_bgr, params)
            return res_img, meta, "Marker-Based Watershed", "Module 4"
        elif op_id == "mean_shift":
            res_img, meta = module4.run_mean_shift(img_bgr, params)
            return res_img, meta, "Mean Shift Clustering", "Module 4"
        elif op_id == "graph_segmentation":
            res_img, meta = module4.run_graph_segmentation(img_bgr, params)
            return res_img, meta, "Felzenszwalb Graph Segmentation", "Module 4"
        elif op_id == "superpixels_slic":
            res_img, meta = module4.run_superpixels_slic(img_bgr, params)
            return res_img, meta, "SLIC Superpixels", "Module 4"

        # Module 5
        elif op_id == "rotation":
            res_img, meta = module5.run_rotation(img_bgr, params)
            return res_img, meta, "2D Rotation", "Module 5"
        elif op_id == "translation":
            res_img, meta = module5.run_translation(img_bgr, params)
            return res_img, meta, "Translation (Shift)", "Module 5"
        elif op_id == "scaling":
            res_img, meta = module5.run_scaling(img_bgr, params)
            return res_img, meta, "Affine Scaling", "Module 5"
        elif op_id == "rigid_transformation":
            res_img, meta = module5.run_rigid_transformation(img_bgr, params)
            return res_img, meta, "Rigid Euclidean Transformation", "Module 5"
        elif op_id == "affine_transformation":
            res_img, meta = module5.run_affine_transformation(img_bgr, params)
            return res_img, meta, "General Affine Transformation", "Module 5"
        elif op_id == "orb_registration":
            res_img, meta = module5.run_orb_alignment_registration(img_bgr, params, second_bgr)
            return res_img, meta, "Feature Registration (ORB+RANSAC)", "Module 5"
        elif op_id == "deformable_registration":
            res_img, meta = module5.run_deformable_registration_demo(img_bgr, params)
            return res_img, meta, "Deformable Registration (Demo)", "Module 5"
        elif op_id == "optical_flow":
            res_img, meta = module5.run_optical_flow_farneback(img_bgr, params, second_bgr)
            return res_img, meta, "Dense Optical Flow (Farneback)", "Module 5"

        else:
            raise ValueError(f"Unknown operation ID: {op_id}")

    def process_image_pipeline(
        self,
        image_id: str,
        operations: List[Dict[str, Any]],
        second_image_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs the requested CV operations on an uploaded image and stores outputs."""
        img_path = self._resolve_image_path(image_id)
        if not img_path or not img_path.exists():
            raise FileNotFoundError(f"Image not found with ID {image_id}")
            
        img_bgr = cv2.imread(str(img_path))
        if img_bgr is None:
            raise ValueError(f"Could not decode image at {img_path}")
            
        second_bgr = None
        if second_image_id:
            sec_path = self._resolve_image_path(second_image_id)
            if sec_path and sec_path.exists():
                second_bgr = cv2.imread(str(sec_path))
                
        results = []
        aggregated_meta = {
            "source_dimensions": f"{img_bgr.shape[1]}x{img_bgr.shape[0]}",
            "source_channels": img_bgr.shape[2],
            "operations_executed": []
        }
        
        for item in operations:
            op_id = item.get("id") or item.get("operation_id")
            params = item.get("params") or item.get("parameters") or {}
            start_t = time.perf_counter()
            try:
                processed_mat, meta, op_name, mod_name = self.execute_operation(op_id, img_bgr, params, second_bgr)
                elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
                
                # Save processed image
                out_filename = f"{image_id}_{op_id}_{uuid.uuid4().hex[:6]}.jpg"
                out_path = PROCESSED_DIR / out_filename
                cv2.imwrite(str(out_path), processed_mat)
                out_url = f"/api/image/processed/{out_filename}"
                
                res_item = {
                    "operation_id": op_id,
                    "operation_name": op_name,
                    "module_name": mod_name,
                    "status": "success",
                    "execution_time_ms": elapsed_ms,
                    "processed_image_url": out_url,
                    "metadata": meta,
                    "error": None
                }
                results.append(res_item)
                aggregated_meta["operations_executed"].append(op_name)
                aggregated_meta[op_id] = meta
                
            except Exception as e:
                elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
                results.append({
                    "operation_id": op_id,
                    "operation_name": op_id,
                    "module_name": "Unknown",
                    "status": "error",
                    "execution_time_ms": elapsed_ms,
                    "processed_image_url": None,
                    "metadata": {},
                    "error": str(e)
                })
                
        return {
            "image_id": image_id,
            "results": results,
            "aggregated_metadata": aggregated_meta
        }

cv_service = CVService()
