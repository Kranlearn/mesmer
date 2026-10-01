# Mesmer v1.0 — Multimodal Affective Computing Core

An experimental R&D command-line and visual utility designed to capture, process, and correlate real-time human biometric signals. By fusing computer vision and digital signal processing (DSP), Mesmer cross-references facial micro-movements with high-frequency acoustic friction to isolate behavioral anomalies and classify subtle affective states, such as contempt or irritation.

## Core Architectures
* **Biometric Signal Processing:** Implements Fast Fourier Transform (FFT) algorithms via `scipy` to extract pitch parameters and monitor human nasal friction signatures (2000 Hz - 8000 Hz).
* **Computer Vision Télémétrie:** Leverages frame-by-frame absolute structural differences (`absdiff`) via OpenCV to isolate spatial pixel fluctuations and log sudden movement peaks.
* **Multimodal Decision Engine:** Anchors asynchronous audio and video streams through localized threading gates to validate concurrent biometric proof and suppress false positives.

## Operational Deployment
To activate the multimodal sensor HUD, run the main fusion pipeline:
```bash
python mesmer_fusion.py
```

## Repository Blueprints
* `mesmer_fusion.py`: Core multimodal engine with synchronized visual/audio telemetry.
* `mesmer_audio.py`: Asynchronous standalone acoustic frequency sniffer.
* `mesmer_vision.py`: Differential frame-by-frame movement monitor.
* `.gitignore`: Built-in runtime and virtual environment overhead shielding.

---
*Developed by Chris Silvina (Kranlearn) for high-efficiency behavioral engineering.*
