# Computer Vision Modules Specification — PromptVision

PromptVision incorporates a full suite of classical and modern Computer Vision algorithms across five core B.Tech syllabus modules. Every operation executes real computational algorithms using OpenCV, NumPy, scikit-image, SciPy, and PyWavelets.

---

## Module 1: Introduction to Computer Vision
Located in: [`backend/app/cv/introduction/module1.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/cv/introduction/module1.py)

| Operation ID | Algorithm Name | Mathematical Formulation / Implementation | Returned Metadata |
|---|---|---|---|
| `rgb_grayscale` | RGB & Grayscale Channel Splitting | $Y = 0.299R + 0.587G + 0.114B$ via `cv2.cvtColor`, channel heatmaps | Channel intensity statistics (min, max, mean, std) |
| `pixel_inspection` | Pixel Stats & Shannon Entropy | $H(X) = -\sum p(i) \log_2 p(i)$ and Viridis intensity heatmap | Shannon entropy (bits), dynamic range, mean intensity |
| `sampling_demo` | Sampling Theorem & Aliasing | Spatial decimation without anti-aliasing vs Gaussian low-pass pre-filtering | Downsampling factor, resolution comparison, MSE distortion |
| `fourier_transform` | 2D Fast Fourier Transform Spectrum | 2D FFT shift and log magnitude $20 \log(\|F(u, v)\| + 1)$ | Low-frequency vs high-frequency energy ratio (%) |
| `wavelet_decomposition` | 2D Haar Wavelet Decomposition | 2D DWT (`pywt.dwt2`) with Haar wavelet | Subband energies for LL, LH, HL, and HH |

---

## Module 2: Image Filtering & Enhancement
Located in: [`backend/app/cv/filtering/module2.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/cv/filtering/module2.py)

| Operation ID | Algorithm Name | Implementation Details | Parameters |
|---|---|---|---|
| `averaging_filter` | Box Averaging Filter | Uniform spatial convolution kernel | `kernel_size` (3 to 25) |
| `gaussian_filter` | Gaussian Smoothing | 2D isotropic Gaussian low-pass filter | `kernel_size`, `sigma` |
| `median_filter` | Median Non-Linear Filter | Order-statistic median filter for impulse noise | `kernel_size` |
| `bilateral_filter` | Bilateral Filter | Edge-preserving radiometric/spatial smoothing | `diameter`, `sigma_color`, `sigma_space` |
| `thresholding` | Image Binarization | Global, Adaptive Mean, Adaptive Gaussian, and Otsu | `mode`, `cutoff` |
| `morphological_ops` | Morphological Operators | Rectangular structuring element Erosion, Dilation, Open, Close | `operation`, `kernel_size`, `iterations` |
| `histogram_equalization` | Histogram Equalization & CLAHE | Contrast-limited adaptive equalization on luminance channel | `method` (`clahe`, `global`), `clip_limit` |
| `jpeg_compression` | JPEG Quantization & PSNR | Multi-tier DCT lossy compression (Q=10, 50, 90) | PSNR (dB) and file size comparison |

---

## Module 3: Feature Detection & Matching
Located in: [`backend/app/cv/features/module3.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/cv/features/module3.py)

| Operation ID | Algorithm Name | Implementation Details | Returned Metadata |
|---|---|---|---|
| `template_matching` | Template Matching | Normalized cross-correlation (`TM_CCOEFF_NORMED`) | Peak correlation score, match coordinates |
| `harris_corners` | Harris Corner Detection | Second-moment auto-correlation eigenvalues | Detected corner count, parameter $k$ |
| `sobel_edges` | Sobel Gradient Magnitude | First-order spatial derivatives along X and Y axes | Mean and max gradient magnitude |
| `canny_edges` | Canny Edge Detection | Multi-stage NMS + dual-threshold hysteresis | Total edge pixels, edge density (%) |
| `laplacian_edges` | Laplacian Focus Sharpness | Isotropic second derivative zero-crossings | Laplacian focus variance, sharpness estimate |
| `grid_detection` | Hough Line Grid Detection | Probabilistic Hough transform accumulator | Detected structural line count |
| `contour_extraction` | Topological Contours | Border following hierarchical contour extraction | Total contours, largest contour area |
| `bounding_boxes` | Salient Bounding Rectangles | Minimum area rotated and axis-aligned bounding boxes | Extracted box count and coordinates |
| `orb_features` | ORB Keypoint Detection | Oriented FAST keypoints with BRIEF descriptors | Keypoints count, descriptor dimensions |
| `orb_matching` | ORB Descriptor Matching | Brute-force Hamming distance matching | Total matches, top match average distance |
| `haar_faces` | Haar Face Detection | Viola-Jones AdaBoost rectangular feature cascade | Detected face bounding boxes (*no identity recognition*) |
| `haar_eyes` | Haar Eye Detection | Haar cascade ocular feature classifier | Detected eye feature count |

---

## Module 4: Image Segmentation
Located in: [`backend/app/cv/segmentation/module4.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/cv/segmentation/module4.py)

| Operation ID | Algorithm Name | Implementation Details | Computational Safeguards |
|---|---|---|---|
| `active_contours` | Active Contours (Snakes) | Energy-minimizing spline attracted to image gradients | Downsamples to max 400px width on CPU |
| `split_and_merge` | Quadtree Split & Merge | Recursive homogeneity variance partitioning | Min block size limit |
| `watershed` | Marker Morphological Watershed | Euclidean distance transform gradient flooding | Prevents over-segmentation |
| `mean_shift` | Mean Shift Mode Seeking | Non-parametric spatial-color clustering | Downsamples to max 500px width |
| `graph_segmentation` | Felzenszwalb Graph-Based | Minimum spanning tree graph component clustering | Downsamples to max 400px width |
| `superpixels_slic` | SLIC Superpixels | CIELAB-spatial 5D k-means superpixel clustering | Compactness weight parameter |

---

## Module 5: Transformation, Alignment & Motion
Located in: [`backend/app/cv/transformations/module5.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/cv/transformations/module5.py)

| Operation ID | Algorithm Name | Implementation Details | Second Image Support |
|---|---|---|---|
| `rotation` | 2D Planar Rotation | Counter-clockwise affine rotation about center | Single image |
| `translation` | Planar Translation | Directional horizontal and vertical coordinate shift | Single image |
| `scaling` | Spatial Rescaling | Isotropic / anisotropic bicubic interpolation | Single image |
| `rigid_transformation` | Rigid Euclidean Isometry | $SE(2)$ Euclidean transform preserving distances | Single image |
| `affine_transformation` | 6-DOF Affine Transform | 3-point coordinate mapping with shear visualization | Single image |
| `orb_registration` | Feature-Based Registration | ORB + RANSAC projective homography alignment | Supports uploaded 2nd target image |
| `deformable_registration` | Deformable Displacement Demo | Elastic non-rigid vector field simulation with quiver vectors | Single image (*educational demo only*) |
| `optical_flow` | Farneback Dense Optical Flow | Dense polynomial expansion flow rendered as HSV wheel | Supports uploaded 2nd sequential image |
