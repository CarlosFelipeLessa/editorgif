# Task Plan: EditorGIF (Video to Transparent Game GIF)

## North Star Metric
Build an end-to-end, game-ready video-to-transparent-GIF processing tool that allows users to upload any video, remove the background using AI frame-by-frame, adjust animation parameters (FPS, duration, resolution, transparency threshold), preview the output over a checkerboard background, and download the resulting transparent GIF (and sprite sheet).

---

## Phase 1: Blueprint & Specification (Data Schemas)
- [x] Define data models: `VideoMetadata`, `ProcessingConfig`, `FrameData`, `OutputResult`.
- [x] Determine core function signatures for `video_processor`, `bg_remover`, `gif_compiler`.
- [x] Establish error handling patterns and fallback logic for CPU/GPU.

## Phase 2: Links & Environment Setup
- [x] Generate `requirements.txt` with tested package pins.
- [x] Install dependencies (`opencv-python`, `onnxruntime`, `rembg`, `streamlit`).
- [x] Validate runtime imports and test ONNX Runtime CPU inference handshake.

## Phase 3: Architecture (Core Business Logic)
- [x] Create `core/video_processor.py`:
  - Video loading, duration/FPS metadata inspection.
  - Interval clipping (`start_time` to `end_time`).
  - FPS downsampling / uniform frame extraction.
  - Dimension scaling / aspect ratio preservation.
- [x] Create `core/bg_remover.py`:
  - Persistent ONNX session caching (`rembg.new_session`).
  - Batch frame processing with progress callback.
  - Edge defringing and alpha thresholding (binary 1-bit matte cleanup).
  - Optional auto-bounding-box crop for character centering.
- [x] Create `core/gif_compiler.py`:
  - Palette quantization with transparency color assignment.
  - `disposal=2` frame handling (restore background) to eliminate ghost trails.
  - Frame duration / delay calculation from target FPS.
  - Game bonus: Optional Sprite Sheet generation (horizontal strip or grid) for direct import in Godot/Unity.

## Phase 4: Stylization (Streamlit Web Interface)
- [x] Create `ui/styles.py`:
  - Cyber-dark gamer theme with glassmorphism touches.
  - CSS checkerboard pattern for transparent canvas preview.
  - Custom styled buttons, sliders, file dropzone, and progress bar.
- [x] Create `ui/app.py`:
  - Two-column responsive layout: Controls & Video Input on Left; Transparent Preview & Download on Right.
  - Video player with time scrubbers (Start / End).
  - Animation tuning: Target FPS (8, 12, 15, 24, 30), Scale slider (25% to 100%), Alpha threshold slider.
  - Live progress feedback during AI segmentation.
  - Interactive preview on checkerboard grid + Instant download button for `.gif` (and sprite sheet).

## Phase 5: Trigger & Deployment
- [x] Create automated launcher batch script `run_app.bat` for 1-click Windows execution.
- [x] Create comprehensive `README.md` with visual architecture diagram and engine guides.
- [x] Create end-to-end synthetic video smoke test (`test_pipeline.py`).

## Phase 6: Renaming to EditorGIF & GitHub Publication
- [x] Rename project across UI, docstrings, launcher, and docs to `EditorGIF`.
- [x] Configure `.gitignore` for Python, Streamlit, and ONNX weights.
- [x] Initialize Git repository, commit code.
- [x] Create remote repository `editorgif` on GitHub via GitHub API.
- [x] Push to `origin main` and verify remote deployment.

## Phase 8: UI/UX Pro Max Redesign
- [x] Apply cyber-dark theme, Google Fonts, and glassmorphism styling in `ui/styles.py`.
- [x] Improve HUD metrics grid and checkerboard preview container.

## Phase 9: GIF Playback Speed Multiplier (Aumentar Velocidade do GIF)
- [x] Add `speed_multiplier` parameter and effective duration calculation in `core/gif_compiler.py`.
- [x] Add speed selector slider (`0.5x` to `3.0x`) in `ui/app.py`.
- [x] Implement instantaneous GIF regeneration and cache invalidation by speed key without re-running AI.
- [x] Update live duration statistics and download filenames with speed tag.
- [x] Update translations in `ui/i18n.py` (PT-BR and EN-US).
- [x] Add automated test assertion in `test_pipeline.py` and verify all tests pass.

## Phase 10: Sprite Sheet Input & Conversion (Sprite Sheet para GIF)
- [x] Implement `slice_sprite_sheet` function in `core/gif_compiler.py` with horizontal strip and grid layout support.
- [x] Add input media toggle (`🎬 Vídeo / GIF` vs `👾 Sprite Sheet`) in `ui/app.py`.
- [x] Implement sprite sheet preview, frame dimensions calculation, column/row configuration, and instant GIF compiler.
- [x] Add optional AI background removal toggle for non-transparent sprite sheets.
- [x] Add automated pipeline test case `[8/8]` in `test_pipeline.py`.
- [x] Update documentation in `README.md`, `progress.md`, and `task_plan.md`.



