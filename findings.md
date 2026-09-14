# Technical Findings & Research Log

## 1. Environment Analysis
- **Operating System**: Windows 11 AMD64
- **Python Version**: Python 3.14.6 (64-bit)
- **Pre-installed Packages**: `pillow 12.3.0`, `imageio 2.37.4`, `numpy 2.5.2`, `customtkinter 6.0.0`, `pygame-ce 2.5.7`.
- **Package Availability Verification**:
  - `opencv-python` (5.0.0.93 cp37-abi3-win_amd64): Available & compatible.
  - `onnxruntime` (1.30.0 cp314-win_amd64): Available & compatible.
  - `rembg` (2.0.84): Available & compatible with PyMatting, pooch, scikit-image.
  - `streamlit` (1.63.0): Available & compatible with altair, pyarrow, pandas.

## 2. GIF Format Transparency Mechanics & Game Engine Quirks
- **GIF 89a Transparency Limitation**: GIF only supports 1-bit binary transparency (either a pixel is 100% transparent or 100% opaque). Semitransparent pixels (alpha 1-254) from soft edge antialiasing in AI segmentation models will turn into unsightly matte fringes (usually dark or white halos) if not thresholded or defringed.
- **Defringing & Alpha Thresholding Strategy**:
  - Apply thresholding (e.g. alpha > 128 is opaque, alpha <= 128 is transparent) OR alpha matting against a neutral background.
  - Optional erosion/dilation to clean up loose edge pixels before palette quantization.
- **Disposal Method `disposal=2` (Restore to background)**:
  - Default GIF players often use `disposal=1` (leave in place), which causes successive frames of moving characters to leave ghost artifacts / trails behind them on transparent backgrounds.
  - Setting `disposal=2` tells the GIF decoder to clear the canvas back to the transparent color before rendering the next frame, ensuring crisp game sprite looping.

## 3. Performance & Memory Optimization
- Ingesting full 1080p 60fps video directly into neural network segmentation can consume high RAM and takes minutes.
- Solutions:
  1. Downscale video frames (e.g., max height 320px or 480px, ideal for game sprites).
  2. Frame rate sampling: sample at 10-15 FPS (normal for 2D game animations), reducing 180 frames (3s video) down to 30-45 frames.
  3. Pre-create a single `new_session()` for `rembg` to keep the ONNX model in memory across all frames instead of initializing on each frame.
  4. Stream results with `st.progress` to give users live frame-by-frame feedback.

## 4. Post-Transparency Temporal Cropping (Zero AI Latency Slicing)
- **Problem**: Re-running AI background segmentation whenever a user wants to shorten or trim the animation by a few frames/seconds is prohibitively slow and wastes GPU/CPU cycles.
- **Solution**: Retain processed RGBA frames (`st.session_state.rgba_frames`) and target FPS in memory.
- **Slicing**: Slicing the pre-segmented list of PIL RGBA images (`frames[start_idx:end_idx]`) and re-quantizing the paletted GIF via Pillow takes < 0.1s.
- **Cache-Keying**: Cache compiled bytes keyed by `(start_idx, end_idx, count)` so that UI reruns and download clicks do not redundantly re-quantize the palette.

