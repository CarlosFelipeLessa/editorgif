"""
End-to-End Test for EditorGIF Pipeline.
Generates a synthetic animation video, processes it through AI background removal,
and validates transparent GIF and sprite sheet generation.
"""
import os
import tempfile
import cv2
import numpy as np
from PIL import Image

from core.video_processor import extract_frames, get_video_metadata
from core.bg_remover import get_rembg_session, process_frames_pipeline
from core.gif_compiler import compile_transparent_gif, compile_sprite_sheet, slice_frames_by_seconds


def generate_synthetic_video(output_path: str, width: int = 160, height: int = 160, fps: int = 10, num_frames: int = 12):
    """
    Creates a synthetic video of a moving character (red & cyan sphere) against a static green screen.
    """
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    try:
        for i in range(num_frames):
            # Static green background
            frame = np.full((height, width, 3), (0, 200, 0), dtype=np.uint8)
            
            # Moving character: circle moving left to right
            center_x = int(30 + (i / num_frames) * (width - 60))
            center_y = int(height / 2 + np.sin(i * 0.5) * 15)
            
            # Draw character head and body
            cv2.circle(frame, (center_x, center_y), 20, (0, 0, 220), -1)  # Red head
            cv2.circle(frame, (center_x, center_y + 15), 10, (220, 220, 0), -1)  # Cyan body
            
            out.write(frame)
    finally:
        out.release()


def run_pipeline_test():
    print("[1/5] Creating synthetic test video...")
    with tempfile.NamedTemporaryFile(suffix="_test.mp4", delete=False) as tf:
        video_path = tf.name

    try:
        generate_synthetic_video(video_path, width=160, height=160, fps=10, num_frames=12)
        assert os.path.exists(video_path), "Failed to create synthetic video."

        print("[2/5] Inspecting video metadata & extracting frames...")
        meta = get_video_metadata(video_path)
        print(f"   Metadata: {meta.width}x{meta.height} | {meta.duration_seconds:.2f}s | {meta.fps} FPS")
        assert meta.width == 160 and meta.height == 160

        frames = extract_frames(
            video_path=video_path,
            start_time=0.0,
            end_time=meta.duration_seconds,
            target_fps=8,
            scale_percent=100
        )
        print(f"   Extracted: {len(frames)} frames.")
        assert len(frames) > 0, "No frames extracted."

        print("[3/5] Loading AI session & removing background...")
        # Use u2net or silueta
        session = get_rembg_session("u2net")
        
        rgba_frames = process_frames_pipeline(
            frames=frames[:4],  # Test with first 4 frames for speedy smoke test
            session=session,
            alpha_threshold=30,
            defringe=True,
            auto_crop=False
        )
        assert len(rgba_frames) == 4, "Segmented frames count mismatch."
        
        # Check transparency in output
        sample_alpha = np.array(rgba_frames[0])[:, :, 3]
        has_transparent_pixels = np.any(sample_alpha == 0)
        has_opaque_pixels = np.any(sample_alpha > 0)
        print(f"   Alpha check: has transparent={has_transparent_pixels}, has opaque={has_opaque_pixels}")
        assert has_transparent_pixels and has_opaque_pixels, "Alpha segmentation failed."

        print("[4/5] Compiling transparent GIF...")
        gif_bytes = compile_transparent_gif(rgba_frames, fps=8)
        assert len(gif_bytes) > 0, "GIF compilation returned empty bytes."
        assert gif_bytes.startswith(b"GIF89a") or gif_bytes.startswith(b"GIF87a"), "Invalid GIF header."
        print(f"   GIF compiled successfully ({len(gif_bytes)} bytes).")

        print("[5/6] Compiling Sprite Sheet...")
        sheet_bytes, sheet_meta = compile_sprite_sheet(rgba_frames, layout="horizontal")
        assert len(sheet_bytes) > 0, "Sprite sheet returned empty bytes."
        assert sheet_meta["frames"] == 4
        print(f"   Sprite sheet created: {sheet_meta['sheet_width']}x{sheet_meta['sheet_height']} px.")

        print("[6/6] Slicing transparent frames by seconds and compiling trimmed GIF & Sprite Sheet...")
        sliced, s_idx, e_idx = slice_frames_by_seconds(rgba_frames, fps=8, start_sec=0.1, end_sec=0.3)
        assert len(sliced) > 0, "Sliced frames list is empty."
        assert len(sliced) <= len(rgba_frames), "Sliced frames exceeded original count."
        trimmed_gif = compile_transparent_gif(sliced, fps=8)
        assert len(trimmed_gif) > 0 and (trimmed_gif.startswith(b"GIF89a") or trimmed_gif.startswith(b"GIF87a")), "Invalid trimmed GIF."
        trimmed_sheet, trimmed_meta = compile_sprite_sheet(sliced, layout="horizontal")
        assert len(trimmed_sheet) > 0 and trimmed_meta["frames"] == len(sliced), "Invalid trimmed sprite sheet."
        print(f"   Trimmed GIF ({len(sliced)} frames, {len(trimmed_gif)} bytes) and sheet ({trimmed_meta['sheet_width']}x{trimmed_meta['sheet_height']}) successfully created.")

        print("\n=== ALL PIPELINE TESTS PASSED ===")

    finally:
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except Exception:
                pass


if __name__ == "__main__":
    run_pipeline_test()
