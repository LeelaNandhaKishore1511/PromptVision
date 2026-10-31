# Contributing to PromptVision

Thank you for your interest in contributing to **PromptVision: An Option-Driven Automated Prompt Engineering and Computer Vision Analysis Framework**!

## Code of Conduct

This project is part of an academic B.Tech Final Year research initiative. We ask that all contributors, testers, and reviewers uphold a respectful, collaborative, and evidence-grounded environment.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LeelaNandhaKishore1511/PromptVision.git
   cd PromptVision
   ```

2. **Backend Setup**:
   ```bash
   pip install -r backend/requirements.txt
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Verify Local Ollama Models**:
   Ensure Ollama is running with `qwen2.5vl:3b`:
   ```bash
   ollama list
   ```

## Pull Request Guidelines

1. **Hardware Considerations**: Any new algorithm or inference path must be tested on CPU inference (Intel Core i5, 16GB RAM) without requiring a dedicated GPU.
2. **Deterministic CV Processing**: All Computer Vision functions must be implemented with real OpenCV / NumPy / scikit-image algorithms and return verifiable metadata. Fabricated outputs or static mock responses are strictly prohibited.
3. **Multi-Strategy Model Parity**: When introducing new prompt strategies, all strategies compared in a single experiment must execute on the **exact same selected Vision-Language Model**.
4. **Testing**: Run the automated test suite before opening a PR:
   ```bash
   python -m unittest discover tests
   python test_system.py
   ```
5. **Code Style**:
   - Python: Follow PEP 8 guidelines.
   - React / JavaScript: Use clean functional components with hooks.
