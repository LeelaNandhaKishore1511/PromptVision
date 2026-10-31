import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

test_dir = Path("test_images")
test_dir.mkdir(exist_ok=True)

# 1. Normal Photograph (Landscape scene)
h, w = 480, 640
photo = np.zeros((h, w, 3), dtype=np.uint8)
# Sky gradient
for y in range(260):
    val = int(240 - y * 0.5)
    photo[y, :] = [val, val - 30, max(0, val - 100)] # BGR: light blue sky
# Sun
cv2.circle(photo, (520, 90), 45, (100, 240, 255), -1)
# Mountains
pts1 = np.array([[0, 260], [180, 130], [360, 260]], np.int32)
cv2.fillPoly(photo, [pts1], (80, 70, 90))
pts2 = np.array([[220, 260], [420, 100], [640, 260]], np.int32)
cv2.fillPoly(photo, [pts2], (100, 90, 110))
# Ground/grass
photo[260:, :] = [40, 130, 50]
# Tree
cv2.rectangle(photo, (140, 240), (160, 360), (30, 50, 80), -1)
cv2.circle(photo, (150, 210), 50, (30, 160, 40), -1)
cv2.imwrite(str(test_dir / "sample_photograph.jpg"), photo)

# 2. Diagram or Chart
chart = np.full((480, 640, 3), 255, dtype=np.uint8)
# Title
cv2.putText(chart, "Quarterly Adoption Analysis (2026)", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2)
# Axes
cv2.line(chart, (80, 400), (580, 400), (50, 50, 50), 2)
cv2.line(chart, (80, 400), (80, 80), (50, 50, 50), 2)
# Grid lines
for y_g in range(120, 400, 60):
    cv2.line(chart, (80, y_g), (580, y_g), (220, 220, 220), 1)
# Bars
bars = [("Q1", 160, (220, 120, 50)), ("Q2", 240, (50, 180, 100)), ("Q3", 310, (50, 120, 230)), ("Q4", 280, (180, 80, 200))]
for idx, (lbl, h_val, color) in enumerate(bars):
    x_b = 130 + idx * 110
    cv2.rectangle(chart, (x_b, 400 - h_val), (x_b + 60, 400), color, -1)
    cv2.putText(chart, lbl, (x_b + 15, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 40, 40), 2)
    cv2.putText(chart, str(h_val), (x_b + 10, 390 - h_val), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 40, 40), 1)
cv2.imwrite(str(test_dir / "sample_chart.png"), chart)

# 3. Image Containing Text (Technical Documentation / Notice)
doc = np.full((520, 640, 3), 250, dtype=np.uint8)
cv2.rectangle(doc, (30, 30), (610, 490), (0, 0, 0), 2)
cv2.putText(doc, "PROMPTVISION RESEARCH FRAMEWORK", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (10, 40, 140), 2)
cv2.putText(doc, "System Protocol: Automated Multi-Strategy Benchmark", (50, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (30, 30, 30), 1)
cv2.putText(doc, "1. Ingest input image and extract visual metadata.", (50, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
cv2.putText(doc, "2. Execute OpenCV feature detection & segmentation.", (50, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
cv2.putText(doc, "3. Synthesize Basic, CO-STAR, and AI-Optimized prompts.", (50, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
cv2.putText(doc, "4. Perform sequential local inference on Ollama VLM.", (50, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
cv2.putText(doc, "5. Record latency, token metrics, and quality ratings.", (50, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
cv2.putText(doc, "Verified Status: 100% Local Inference (Intel Core i5)", (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (10, 120, 40), 2)
cv2.imwrite(str(test_dir / "sample_text_document.png"), doc)

# 4. Simple Grayscale Image (Geometric shapes & gradients)
gray_img = np.zeros((400, 500), dtype=np.uint8)
for i in range(500):
    gray_img[:, i] = int(i * 255 / 500) # horizontal gradient
cv2.circle(gray_img, (140, 200), 70, 240, -1)
cv2.circle(gray_img, (140, 200), 40, 30, -1)
cv2.rectangle(gray_img, (280, 120), (440, 280), 60, -1)
cv2.rectangle(gray_img, (310, 150), (410, 250), 210, -1)
cv2.imwrite(str(test_dir / "sample_grayscale.png"), gray_img)

print("ALL 4 TEST IMAGES CREATED SUCCESSFULLY IN test_images/")
