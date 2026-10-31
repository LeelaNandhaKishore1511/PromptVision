import unittest
import numpy as np
import cv2
import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.cv.introduction import module1
from app.cv.filtering import module2
from app.cv.features import module3
from app.cv.segmentation import module4
from app.cv.transformations import module5
from app.cv.cv_service import cv_service

class TestComputerVisionEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a synthetic 160x160 RGB test image
        cls.img_bgr = np.zeros((160, 160, 3), dtype=np.uint8)
        # Background gradient
        for y in range(160):
            cls.img_bgr[y, :, 0] = y
            cls.img_bgr[:, y, 1] = 160 - y
            cls.img_bgr[y, :, 2] = 120
        # Foreground geometric circle and rectangle
        cv2.circle(cls.img_bgr, (80, 80), 30, (255, 255, 255), -1)
        cv2.rectangle(cls.img_bgr, (20, 20), (50, 50), (0, 0, 255), -1)

    # MODULE 1 TESTS
    def test_module1_rgb_grayscale(self):
        res, meta = module1.run_rgb_grayscale(self.img_bgr, {})
        self.assertIsNotNone(res)
        self.assertEqual(meta["channel_count"], 3)
        self.assertIn("grayscale_stats", meta)

    def test_module1_pixel_inspection(self):
        res, meta = module1.run_pixel_inspection(self.img_bgr, {})
        self.assertIsNotNone(res)
        self.assertIn("shannon_entropy", meta)
        self.assertGreater(meta["shannon_entropy"], 0)

    def test_module1_sampling_demo(self):
        res, meta = module1.run_sampling_demonstration(self.img_bgr, {"factor": 4})
        self.assertIsNotNone(res)
        self.assertEqual(meta["downsampling_factor"], 4)

    def test_module1_fourier_transform(self):
        res, meta = module1.run_fourier_transform(self.img_bgr, {})
        self.assertIsNotNone(res)
        self.assertIn("low_frequency_energy_percentage", meta)

    def test_module1_wavelet_decomposition(self):
        res, meta = module1.run_wavelet_decomposition(self.img_bgr, {})
        self.assertIsNotNone(res)
        self.assertIn("energy_ll", meta)

    # MODULE 2 TESTS
    def test_module2_gaussian_filter(self):
        res, meta = module2.run_gaussian_filter(self.img_bgr, {"kernel_size": 5, "sigma": 1.2})
        self.assertEqual(res.shape, self.img_bgr.shape)
        self.assertEqual(meta["sigma"], 1.2)

    def test_module2_thresholding_otsu(self):
        res, meta = module2.run_thresholding(self.img_bgr, {"mode": "otsu"})
        self.assertIsNotNone(res)
        self.assertIn("calculated_threshold_value", meta)

    def test_module2_morphological_ops(self):
        res, meta = module2.run_morphological_ops(self.img_bgr, {"operation": "opening", "kernel_size": 3})
        self.assertEqual(res.shape, self.img_bgr.shape)

    def test_module2_clahe(self):
        res, meta = module2.run_histogram_equalization(self.img_bgr, {"method": "clahe", "clip_limit": 2.0})
        self.assertEqual(res.shape, self.img_bgr.shape)

    def test_module2_jpeg_compression(self):
        res, meta = module2.run_jpeg_compression_comparison(self.img_bgr, {})
        self.assertIsNotNone(res)
        self.assertIn("q90_psnr_db", meta)

    # MODULE 3 TESTS
    def test_module3_canny_edges(self):
        res, meta = module3.run_canny_edges(self.img_bgr, {"low_threshold": 50, "high_threshold": 150})
        self.assertIn("edge_density_pct", meta)
        self.assertGreater(meta["edge_density_pct"], 0)

    def test_module3_contour_extraction(self):
        res, meta = module3.run_contour_extraction(self.img_bgr, {})
        self.assertIn("total_contours_found", meta)
        self.assertGreater(meta["total_contours_found"], 0)

    def test_module3_orb_features(self):
        res, meta = module3.run_orb_features(self.img_bgr, {"n_features": 200})
        self.assertIn("keypoints_detected", meta)

    def test_module3_laplacian_sharpness(self):
        res, meta = module3.run_laplacian_edges(self.img_bgr, {})
        self.assertIn("laplacian_variance_focus_measure", meta)

    # MODULE 4 TESTS
    def test_module4_split_merge(self):
        res, meta = module4.run_split_and_merge(self.img_bgr, {"var_threshold": 25.0, "min_size": 8})
        self.assertIn("leaf_regions_count", meta)

    def test_module4_watershed(self):
        res, meta = module4.run_watershed(self.img_bgr, {})
        self.assertIn("identified_catchment_basins", meta)

    def test_module4_slic_superpixels(self):
        res, meta = module4.run_superpixels_slic(self.img_bgr, {"n_segments": 30})
        self.assertIn("actual_superpixels_formed", meta)

    # MODULE 5 TESTS
    def test_module5_rotation(self):
        res, meta = module5.run_rotation(self.img_bgr, {"angle": 45.0})
        self.assertEqual(res.shape, self.img_bgr.shape)
        self.assertEqual(meta["angle_degrees"], 45.0)

    def test_module5_rigid_transformation(self):
        res, meta = module5.run_rigid_transformation(self.img_bgr, {"angle": 15.0, "dx": 10.0, "dy": -5.0})
        self.assertEqual(res.shape, self.img_bgr.shape)

    def test_module5_affine_transformation(self):
        res, meta = module5.run_affine_transformation(self.img_bgr, {"shear": 0.1})
        self.assertEqual(res.shape, self.img_bgr.shape)

    def test_module5_optical_flow(self):
        res, meta = module5.run_optical_flow_farneback(self.img_bgr, {})
        self.assertIsNotNone(res)
        self.assertIn("mean_motion_velocity_px", meta)

if __name__ == "__main__":
    unittest.main()
