# Security Policy — PromptVision

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Local Privacy & Data Boundary Guarantee

**PromptVision** is engineered from the ground up as a **100% offline, privacy-first local application**:
1. **Zero External Cloud Egress**: Uploaded visual images, Computer Vision metadata, and generated responses are processed exclusively on the user's local machine via localhost (`127.0.0.1`).
2. **Local AI Inference**: Model execution runs directly against the user's local Ollama instance (`http://localhost:11434`). No API keys, cloud credits, or third-party servers are queried.
3. **Local Database Storage**: All experiment histories, quiz scores, and evaluation ratings are written strictly to local SQLite (`backend/data/promptvision.db`).
4. **Biometric Safeguard**: Facial analysis in Computer Vision Module 3 uses Haar cascades solely for rectangular face/eye geometry bounding boxes. The framework explicitly forbids and does not implement facial recognition, biometric identity classification, or personal identification.

## Reporting a Vulnerability

If you discover a security vulnerability or accidental credential/data leakage risk within the PromptVision repository, please open a private security advisory on GitHub or email the project maintainer at `leelanandhakishore1511@gmail.com`.
