# Project Constitution: EditorGIF (Video to Transparent Game GIF)

## 1. Project Identity & Purpose
`EditorGIF` is a high-performance multimedia tool designed for indie game developers, animators, and digital artists. It converts recorded video clips (MP4, WebM, MOV, AVI) into game-ready transparent GIFs and spritesheets with AI-powered background removal (rembg/BiRefNet/U2-Net), precise frame rate sampling, frame cropping, and palette-quantized alpha transparency without ghosting.

## 2. Core Architectural Principles
- **Data-First Architecture**: Clean separation between video frame ingestion (`video_processor`), AI segmentation (`bg_remover`), GIF/Sprite compilation (`gif_compiler`), and UI presentation layer.
- **Game Engine Standard Compliance**:
  - Binary/alpha matte defringing to eliminate edge artifacts and white halos.
  - Frame disposal method set to `disposal=2` (restore to background) to prevent frame ghosting/trailing.
  - Consistent frame dimensions, bounds alignment, and optional auto-cropping to character bounding box.
  - Variable frame rate (FPS) targeting game timing (8, 12, 15, 24, 30 FPS).
- **Non-blocking Execution**: Asynchronous or batched frame processing with real-time UI progress feedback.
- **Resource Hygiene**: In-memory byte streaming (`io.BytesIO`) wherever possible to prevent temporary disk pollution.

## 3. Technology Stack
- **Runtime**: Python 3.10+ (tested on Python 3.14.6 x64 Windows)
- **Computer Vision & Video**: OpenCV (`opencv-python`), Pillow (`PIL`), ImageIO
- **AI Background Removal**: `rembg` with ONNX Runtime (`onnxruntime`) using models such as `u2net`, `isnet-general-use`, or `birefnet-general`
- **User Interface**: `Streamlit` with modern dark cyber-gaming styling, checkerboard transparency preview canvas, and instant download buttons.

## 4. Governance & File Structure
```
sprite-animator-pro-source/
├── core/
│   ├── __init__.py
│   ├── video_processor.py    # Video loading, time trimming, FPS resample, resolution scaling
│   ├── bg_remover.py         # AI background segmentation session & alpha mask post-processing
│   └── gif_compiler.py       # Transparent GIF & Spritesheet compilation with palette optimization
├── ui/
│   ├── __init__.py
│   ├── app.py                # Streamlit user interface, state management, checkerboard preview
│   └── styles.py             # Custom CSS styling (dark gaming theme, checkerboard grid)
├── samples/                  # Optional sample assets & tests
├── requirements.txt          # Production dependencies
├── run_app.bat               # Windows quick-launch script
├── gemini.md                 # Project constitution & rules
├── task_plan.md              # BLAST phases & progress tracking
├── findings.md               # Technical discoveries, performance notes
└── progress.md               # Execution log and verification results
```
