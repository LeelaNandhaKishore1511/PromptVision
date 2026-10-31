# Computer Vision Syllabus Mapping — PromptVision

This document specifies the mapping of the 5 Computer Vision syllabus modules implemented within the PromptVision framework. Every operation is backed by real OpenCV, NumPy, SciPy, scikit-image, and PyWavelets algorithms.

---

## MODULE 1: Introduction to Computer Vision

### Syllabus Coverage
- Digital images, image formation, and representation.
- Sampling theorem, Nyquist limit, and aliasing.
- Frequency-domain representation (2D Fourier Transform).
- Multi-resolution analysis (Wavelet Transforms).

### Implemented Algorithms (`backend/app/cv/introduction/module1.py`)
1. **RGB & Grayscale Representation (`rgb_grayscale`)**:
   - Decomposes color images into discrete Red, Green, and Blue intensity arrays.
   - Computes grayscale luminance using standard CIE photometric weights:
     $$Y = 0.299R + 0.587G + 0.114B$$
   - Visualizes channel-specific color heatmaps.
2. **Pixel Intensity Inspection (`pixel_inspection`)**:
   - Calculates statistical metrics: dynamic range, minimum, maximum, mean, median, and standard deviation.
   - Computes Shannon Information Entropy:
     $$H(X) = -\sum_{i=0}^{255} p(i) \log_2 p(i)$$
3. **Sampling Theorem & Aliasing Demonstration (`sampling_demo`)**:
   - Demonstrates spatial decimation by factors of 2x, 4x, 8x, and 16x.
   - Demonstrates aliasing artifacts (moiré, staircasing) caused by violating the Nyquist-Shannon sampling limit versus anti-aliased low-pass Gaussian pre-filtering.
4. **2D Fast Fourier Transform Spectrum (`fourier_transform`)**:
   - Implements 2D Discrete Fourier Transform:
     $$F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) e^{-j 2\pi (\frac{ux}{M} + \frac{vy}{N})}$$
   - Centralizes zero-frequency DC component via `fftshift`.
   - Computes log magnitude spectrum: $S(u, v) = 20 \log(|F(u, v)| + 1)$ and calculates low-frequency vs high-frequency spectral energy ratios.
5. **2D Haar Wavelet Decomposition (`wavelet_decomposition`)**:
   - Decomposes 2D spatial signals via discrete Haar wavelet filters (`pywt.dwt2`).
   - Produces 4 distinct subbands:
     - **LL**: Low-Low approximation subband.
     - **LH**: Horizontal high-frequency detail subband.
     - **HL**: Vertical high-frequency detail subband.
     - **HH**: Diagonal high-frequency detail subband.

---

## MODULE 2: Image Filtering & Enhancement

### Syllabus Coverage
- Spatial filtering (Linear and Non-Linear).
- Image thresholding (Global, Adaptive, and Otsu).
- Morphological operators (Erosion, Dilation, Opening, Closing).
- Contrast enhancement and Histogram Equalization.
- Image compression artifacts.

### Implemented Algorithms (`backend/app/cv/filtering/module2.py`)
1. **Averaging (Box) Spatial Filter (`averaging_filter`)**:
   - Uniform $N \times N$ spatial box convolution kernel for high-frequency noise attenuation.
2. **Gaussian Smoothing Filter (`gaussian_filter`)**:
   - 2D isotropic Gaussian kernel with configurable standard deviation $\sigma$:
     $$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}$$
3. **Median Non-Linear Filter (`median_filter`)**:
   - Order-statistic median filter replacing each pixel with the neighborhood median, eliminating impulse salt-and-pepper noise while preserving sharp boundaries.
4. **Bilateral Edge-Preserving Filter (`bilateral_filter`)**:
   - Combines spatial geometric closeness and radiometric color difference weights to smooth textures while strictly preserving salient edges.
5. **Image Thresholding (`thresholding`)**:
   - Global binary thresholding at arbitrary cutoffs.
   - Adaptive Mean and Adaptive Gaussian thresholding for non-uniform illumination.
   - Otsu's thresholding, maximizing inter-class variance $\sigma_B^2(t)$.
6. **Morphological Operators (`morphological_ops`)**:
   - Erosion ($A \ominus B$) and Dilation ($A \oplus B$).
   - Morphological Opening ($(A \ominus B) \oplus B$) for removing isolated foreground noise.
   - Morphological Closing ($(A \oplus B) \ominus B$) for filling holes and bridging narrow breaks.
7. **Histogram Equalization & CLAHE (`histogram_equalization`)**:
   - Global histogram equalization across the luminance channel (Y in YCrCb).
   - Contrast Limited Adaptive Histogram Equalization (CLAHE) with tileGridSize preventing over-amplification of noise.
8. **JPEG Quantization & Rate-Distortion Analysis (`jpeg_compression`)**:
   - Simulates DCT block quantization at quality factors Q=10, Q=50, and Q=90.
   - Calculates Peak Signal-to-Noise Ratio (PSNR) and file size compression ratios.

---

## MODULE 3: Feature Detection & Matching

### Syllabus Coverage
- Template matching.
- Corner detection (Harris).
- Differential edge detection (Sobel, Canny, Laplacian).
- Hough line and grid detection.
- Contour extraction and bounding boxes.
- Keypoint descriptors (ORB) and matching.
- Haar cascade object detection.

### Implemented Algorithms (`backend/app/cv/features/module3.py`)
1. **Normalized Cross-Correlation Template Matching (`template_matching`)**:
   - Computes normalized cross-correlation:
     $$R(x, y) = \frac{\sum (T \cdot I)}{\sqrt{\sum T^2 \cdot \sum I^2}}$$
   - Locates peak match coordinates with a visual bounding box.
2. **Harris Corner Detection (`harris_corners`)**:
   - Analyzes second-moment auto-correlation matrix $M$:
     $$R = \det(M) - k \cdot (\text{trace}(M))^2$$
   - Detects salient rotation-invariant corners.
3. **Sobel Gradient Vector Magnitude (`sobel_edges`)**:
   - Computes first-order spatial derivatives along horizontal ($G_x$) and vertical ($G_y$) axes.
   - Computes continuous gradient vector magnitude: $G = \sqrt{G_x^2 + G_y^2}$.
4. **Canny Multi-Stage Edge Detector (`canny_edges`)**:
   - Full 4-stage pipeline: Gaussian blur, Sobel gradient, Non-Maximum Suppression (NMS), and dual-threshold hysteresis.
   - Computes total edge pixels and percentage edge density.
5. **Laplacian Second-Derivative & Focus Variance (`laplacian_edges`)**:
   - Computes isotropic second derivative $\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$.
   - Calculates Laplacian variance as a standard quantitative measure of image focus/blur.
6. **Probabilistic Hough Line & Grid Detection (`grid_detection`)**:
   - Transforms edge points into parametric Hough accumulator space $(\rho, \theta)$.
   - Detects rectilinear line segments and structural axes.
7. **Topological Contour Extraction (`contour_extraction`)**:
   - Boundary following algorithm extracting hierarchical contours, perimeter, and area.
8. **Salient Object Bounding Box Extraction (`bounding_boxes`)**:
   - Computes axis-aligned and minimum-area rotated bounding rectangles.
9. **ORB Feature Keypoints & Orientations (`orb_features`)**:
   - Oriented FAST keypoint detector with scale pyramid and intensity centroid orientation.
10. **ORB Feature Descriptor Matching (`orb_matching`)**:
    - Matches 256-bit binary BRIEF descriptors across image pairs using Hamming distance.
11. **Haar Cascade Face Detection (`haar_faces`)**:
    - Viola-Jones AdaBoost rectangular feature cascade for frontal face bounding regions.
    - *Academic Note: Explicitly detects structural face geometry without biometric identification.*
12. **Haar Cascade Eye Detection (`haar_eyes`)**:
    - Detects ocular feature regions within image frames.

---

## MODULE 4: Image Segmentation

### Syllabus Coverage
- Active contours (Snakes).
- Hierarchical split-and-merge.
- Morphological watershed.
- Mean Shift clustering.
- Graph-based segmentation (Felzenszwalb).
- Superpixel representation and Normalized Cut proxies.

### Implemented Algorithms (`backend/app/cv/segmentation/module4.py`)
1. **Active Contours / Snakes (`active_contours`)**:
   - Kass et al. energy-minimizing parametric spline:
     $$E_{\text{snake}} = \int [E_{\text{internal}}(v(s)) + E_{\text{image}}(v(s))] ds$$
   - Balances elasticity ($\alpha$), rigidity ($\beta$), and gradient attraction.
2. **Quadtree Hierarchical Split-and-Merge (`split_and_merge`)**:
   - Recursively subdivides non-homogeneous quadrants when standard deviation exceeds variance threshold, until leaves satisfy homogeneity criteria.
3. **Marker-Controlled Morphological Watershed (`watershed`)**:
   - Computes Euclidean distance transform on binary foreground.
   - Floods gradient relief map from markers to partition touching boundaries without oversegmentation.
4. **Mean Shift Mode Seeking (`mean_shift`)**:
   - Non-parametric kernel density estimation clustering pixels towards local density modes in joint 5D spatial-range space $(x, y, L, a, b)$.
5. **Felzenszwalb-Huttenlocher Graph-Based Segmentation (`graph_segmentation`)**:
   - Kruskal-style minimum spanning tree edge-weight segmentation with scale threshold parameter $k$.
6. **SLIC Superpixel Segmentation (`superpixels_slic`)**:
   - Simple Linear Iterative Clustering generating compact, boundary-adherent superpixel clusters as a low-dimensional graph representation for Normalized Cuts.

---

## MODULE 5: Transformation, Alignment & Motion

### Syllabus Coverage
- 2D Planar transformations (Rigid and Affine).
- Feature-based image registration.
- Deformable registration modeling.
- Dense optical flow.

### Implemented Algorithms (`backend/app/cv/transformations/module5.py`)
1. **Planar Rotation (`rotation`)**:
   - Rotation about arbitrary pivot point with reflection boundary extension.
2. **Planar Translation (`translation`)**:
   - Horizontal ($dx$) and vertical ($dy$) shift matrices.
3. **Affine Spatial Scaling (`scaling`)**:
   - Isotropic and anisotropic scaling using bicubic interpolation.
4. **Rigid Euclidean Isometry (`rigid_transformation`)**:
   - Special Euclidean group $SE(2)$ transformation (3 degrees of freedom: 1 rotation, 2 translations), strictly preserving Euclidean distances and angles.
5. **General 6-DOF Affine Transformation (`affine_transformation`)**:
   - 3-point affine coordinate mapping preserving parallelism, ratios of lengths, and collinearity.
6. **Feature-Based Image Registration (`orb_registration`)**:
   - Extracts ORB descriptors from moving and reference images.
   - Computes robust projective homography using RANSAC (Random Sample Consensus) to register and align image coordinates.
7. **Simplified Deformable Registration (`deformable_registration`)**:
   - Simulates smooth elastic displacement vector fields ($\Delta x, \Delta y$) with vector quiver representation.
   - *Academic Note: Labeled as an educational demonstration of displacement field mechanics, not certified clinical registration.*
8. **Gunnar Farneback Dense Optical Flow (`optical_flow`)**:
   - Approximates local neighborhood frames using quadratic polynomial expansion.
   - Computes dense motion velocity fields visualized via an HSV color wheel (Hue = motion direction, Value = velocity magnitude).
