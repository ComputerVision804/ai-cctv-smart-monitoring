# ai-cctv-smart-monitoring
AI-powered CCTV Smart Monitoring System with real-time multi-camera streams, heatmaps, and event alerts.

# AI CCTV Smart Monitoring System

This is an **AI-powered CCTV Smart Monitoring System** that provides **real-time surveillance** with multiple cameras, intelligent alerts, and interactive dashboards. Built using **Python, OpenCV, YOLOv8, and Flask**, this system demonstrates how AI can enhance security monitoring.

## Features
- **Real-time multi-camera monitoring** – Supports Main and Back camera live feeds.
- **Intelligent detection** – Detects loitering, fights, and crowd alerts.
- **Heatmaps** – Visualizes movement patterns and crowd density.
- **Event alerts** – Automatically saves screenshots and records video when suspicious activity is detected.
- **Snapshot capture** – Manual and automatic photo capture.
- **Recorded video upload** – Analyze pre-recorded footage with AI detection.#
- pip install -r requirements.txt

## Tech Stack
- Python, OpenCV
- YOLOv8 (Ultralytics)
- Flask (Web Dashboard)
- HTML, CSS, Bootstrap (Frontend)
- Matplotlib (Optional for plotting)

## Getting Started
1. Clone the repository:
```bash
git clone https://github.com/ComputerVision804/ai-cctv-smart-monitoring.git
ai-cctv-smart-monitoring/
│
├── app.py                  # Main Flask app
├── camera.py               # Multi-camera handler
├── tracker.py              # Person tracking using DeepSort
├── loitering.py            # Loitering detection logic
├── fight_detection.py      # Fight detection logic
├── alerts.py               # Screenshot and recording handling
├── heatmap.py              # Heatmap generation per camera
├── requirements.txt        # All dependencies
├── videos/                 # Pre-recorded video uploads
├── static/
│   ├── screenshots/        # Saved alert images
│   ├── recordings/         # Event video recordings
│   ├── heatmaps/           # Heatmap images
│   └── snapshots/          # Manual photo snapshots
└── templates/
    └── dashboard.html      # Web dashboard template
