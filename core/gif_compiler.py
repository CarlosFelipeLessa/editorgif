"""
GIF & Sprite Sheet Compiler Module for EditorGIF.
Handles palette quantization, alpha transparency mapping, frame disposal (disposal=2),
and optional Sprite Sheet / Animated WebP generation for game engines.
"""
import io
import math
from typing import List, Optional, Tuple
import numpy as np
from PIL import Image


def _convert_rgba_to_transparent_palette(frame: Image.Image) -> Image.Image:
    """
    Converts an RGBA PIL image to a paletted 'P' image with a dedicated transparent index.
    Guarantees that transparent areas do not turn black or create artifact halos.
    """
    if frame.mode != "RGBA":
        frame = frame.convert("RGBA")

    # Split channels
    r, g, b, a = frame.split()

    # Binary alpha mask: transparent where alpha == 0
    alpha_mask = np.array(a) == 0

    # Quantize RGB channels to 255 colors (reserving 1 index for transparency)
    rgb_img = Image.merge("RGB", (r, g, b))
    paletted = rgb_img.quantize(colors=255, method=Image.Quantize.MEDIANCUT)

    # Palette array is 768 bytes (256 * 3)
    palette = paletted.getpalette()
    if palette is None:
        palette = [0] * 768

    # Reserve index 255 for pure transparency
    transparent_idx = 255
    palette[transparent_idx * 3: transparent_idx * 3 + 3] = [0, 0, 0]

    # Map transparent pixels in the pixel array to transparent_idx
    pixels = np.array(paletted)
    pixels[alpha_mask] = transparent_idx

    # Reconstruct 'P' image
    result = Image.fromarray(pixels, mode="P")
    result.putpalette(palette)
    result.info["transparency"] = transparent_idx
    result.info["disposal"] = 2  # 2 = Clear frame to background (prevents ghosting)

    return result


def compile_transparent_gif(
    frames: List[Image.Image],
    fps: int = 12,
    loop: int = 0
) -> bytes:
    """
    Compiles a list of RGBA frames into an animated GIF with transparent background.

    Args:
        frames: List of RGBA PIL images.
        fps: Playback frames per second.
        loop: Loop count (0 = infinite loop).

    Returns:
        Bytes buffer containing the compiled GIF file.
    """
    if not frames:
        raise ValueError("Frames list cannot be empty.")

    duration_ms = max(20, int(round(1000.0 / fps)))

    paletted_frames = [_convert_rgba_to_transparent_palette(f) for f in frames]

    buffer = io.BytesIO()
    first_frame = paletted_frames[0]

    # Save all frames
    first_frame.save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=paletted_frames[1:],
        duration=duration_ms,
        loop=loop,
        transparency=255,
        disposal=2,
        optimize=False  # optimize=True can corrupt disposal=2 frames in some Pillow versions
    )

    buffer.seek(0)
    return buffer.getvalue()


def compile_sprite_sheet(
    frames: List[Image.Image],
    layout: str = "horizontal",
    max_columns: Optional[int] = None
) -> Tuple[bytes, dict]:
    """
    Stitches frames into a single RGBA PNG sprite sheet for direct use in Unity/Godot.

    Args:
        frames: List of RGBA PIL Images of uniform size.
        layout: 'horizontal' (1 row) or 'grid'.
        max_columns: Number of columns for grid layout (if layout is 'grid').

    Returns:
        Tuple of (PNG bytes buffer, metadata dictionary with frame count and dimensions).
    """
    if not frames:
        raise ValueError("Frames list cannot be empty.")

    num_frames = len(frames)
    frame_w, frame_h = frames[0].size

    if layout == "horizontal" or num_frames == 1:
        cols = num_frames
        rows = 1
    else:
        if max_columns is None or max_columns <= 0:
            cols = math.ceil(math.sqrt(num_frames))
        else:
            cols = min(max_columns, num_frames)
        rows = math.ceil(num_frames / cols)

    sheet_w = cols * frame_w
    sheet_h = rows * frame_h

    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    for idx, frame in enumerate(frames):
        c = idx % cols
        r = idx // cols
        x = c * frame_w
        y = r * frame_h
        sheet.paste(frame, (x, y))

    buffer = io.BytesIO()
    sheet.save(buffer, format="PNG")
    buffer.seek(0)

    metadata = {
        "frames": num_frames,
        "frame_width": frame_w,
        "frame_height": frame_h,
        "sheet_width": sheet_w,
        "sheet_height": sheet_h,
        "columns": cols,
        "rows": rows
    }

    return buffer.getvalue(), metadata


def compile_animated_webp(
    frames: List[Image.Image],
    fps: int = 12,
    loop: int = 0
) -> bytes:
    """
    Compiles frames into an animated WebP with full 8-bit alpha channel support.
    """
    if not frames:
        raise ValueError("Frames list cannot be empty.")

    duration_ms = max(20, int(round(1000.0 / fps)))
    buffer = io.BytesIO()

    frames[0].save(
        buffer,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=loop,
        lossless=True,
        quality=100,
        method=4
    )

    buffer.seek(0)
    return buffer.getvalue()
