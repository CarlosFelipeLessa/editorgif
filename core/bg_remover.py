"""
AI Background Removal & Alpha Matte Refinement Module for EditorGIF.
Uses neural network segmentation (rembg / ONNX) with game-tailored alpha thresholding and defringing.
"""
from typing import Callable, List, Optional, Tuple
import numpy as np
from PIL import Image, ImageFilter
import rembg


_CACHED_SESSIONS = {}


def get_rembg_session(model_name: str = "u2net"):
    """
    Retrieves or creates a cached rembg ONNX session.
    Supported models: 'u2net', 'isnet-general-use', 'birefnet-general', 'silueta'
    """
    global _CACHED_SESSIONS
    if model_name not in _CACHED_SESSIONS:
        _CACHED_SESSIONS[model_name] = rembg.new_session(model_name)
    return _CACHED_SESSIONS[model_name]


def clean_alpha_matte(
    rgba_image: Image.Image,
    alpha_threshold: int = 30,
    defringe: bool = True
) -> Image.Image:
    """
    Cleans up the alpha channel to eliminate halos and noise for 1-bit GIF transparency.

    Args:
        rgba_image: PIL Image in RGBA mode.
        alpha_threshold: Threshold (0-255). Pixels below this become 0 (transparent);
                         pixels above become 255 (fully opaque).
        defringe: If True, cleans edge pixels to avoid color halos.

    Returns:
        Cleaned PIL Image in RGBA mode.
    """
    img_array = np.array(rgba_image).copy()
    if img_array.shape[2] != 4:
        return rgba_image

    r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]

    # Binary alpha thresholding for clean GIF edges
    if alpha_threshold > 0:
        binary_mask = a >= alpha_threshold
        a[binary_mask] = 255
        a[~binary_mask] = 0

    if defringe:
        # Zero-out RGB values for fully transparent pixels to avoid palette bleed
        transparent_pixels = a == 0
        r[transparent_pixels] = 0
        g[transparent_pixels] = 0
        b[transparent_pixels] = 0

    cleaned_array = np.stack([r, g, b, a], axis=-1)
    return Image.fromarray(cleaned_array, mode="RGBA")


def remove_background_single(
    image: Image.Image,
    session=None,
    alpha_threshold: int = 30,
    defringe: bool = True
) -> Image.Image:
    """
    Removes the background from a single frame and applies edge cleanup.
    """
    if session is None:
        session = get_rembg_session()

    # rembg requires RGB or RGBA PIL image
    if image.mode != "RGB" and image.mode != "RGBA":
        image = image.convert("RGB")

    raw_segmented = rembg.remove(image, session=session)
    cleaned = clean_alpha_matte(raw_segmented, alpha_threshold=alpha_threshold, defringe=defringe)
    return cleaned


def find_common_bounding_box(frames: List[Image.Image], padding: int = 4) -> Optional[Tuple[int, int, int, int]]:
    """
    Calculates a unified bounding box across all frames where the character appears,
    preserving animation positioning across cycles while eliminating empty margins.
    """
    min_x, min_y, max_x, max_y = 999999, 999999, 0, 0
    found_any = False

    for frame in frames:
        bbox = frame.getbbox()
        if bbox:
            found_any = True
            min_x = min(min_x, bbox[0])
            min_y = min(min_y, bbox[1])
            max_x = max(max_x, bbox[2])
            max_y = max(max_y, bbox[3])

    if not found_any:
        return None

    # Apply padding within frame boundaries
    width, height = frames[0].size
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    max_x = min(width, max_x + padding)
    max_y = min(height, max_y + padding)

    return (min_x, min_y, max_x, max_y)


def process_frames_pipeline(
    frames: List[Image.Image],
    session=None,
    alpha_threshold: int = 30,
    defringe: bool = True,
    auto_crop: bool = False,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> List[Image.Image]:
    """
    Processes a list of frames through AI background removal with real-time progress.
    """
    if session is None:
        session = get_rembg_session()

    total = len(frames)
    processed_frames: List[Image.Image] = []

    for idx, frame in enumerate(frames):
        if progress_callback:
            progress_callback(idx + 1, total, f"Segmenting frame {idx + 1} of {total}...")

        rgba_frame = remove_background_single(
            frame,
            session=session,
            alpha_threshold=alpha_threshold,
            defringe=defringe
        )
        processed_frames.append(rgba_frame)

    if auto_crop and processed_frames:
        bbox = find_common_bounding_box(processed_frames)
        if bbox:
            processed_frames = [f.crop(bbox) for f in processed_frames]

    return processed_frames
