"""
Video Processor Module for EditorGIF.
Handles video ingestion, metadata extraction, time trimming, frame rate resampling, and dimension scaling.
"""
from dataclasses import dataclass
from typing import List, Optional
import cv2
import numpy as np
from PIL import Image


@dataclass
class VideoMetadata:
    width: int
    height: int
    fps: float
    duration_seconds: float
    total_frames: int


def get_video_metadata(video_path: str) -> VideoMetadata:
    """
    Extracts metadata from a video file.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Guard against zero or NaN FPS
        if fps <= 0 or np.isnan(fps):
            fps = 30.0
        
        duration = total_frames / fps if total_frames > 0 else 0.0

        return VideoMetadata(
            width=width,
            height=height,
            fps=fps,
            duration_seconds=duration,
            total_frames=total_frames
        )
    finally:
        cap.release()


def extract_frames(
    video_path: str,
    start_time: float = 0.0,
    end_time: Optional[float] = None,
    target_fps: int = 12,
    scale_percent: int = 100,
    max_frames: int = 120
) -> List[Image.Image]:
    """
    Extracts, trims, resamples FPS, and rescales video frames into PIL RGB Images.

    Args:
        video_path: Path to the video file.
        start_time: Start timestamp in seconds.
        end_time: End timestamp in seconds (defaults to video duration).
        target_fps: Target frames per second for game animation (e.g. 8, 12, 15, 24).
        scale_percent: Percentage to rescale dimensions (10% to 100%).
        max_frames: Safety limit to prevent memory exhaustion on long clips.

    Returns:
        List of PIL Image objects in RGB format.
    """
    meta = get_video_metadata(video_path)
    if end_time is None or end_time > meta.duration_seconds or end_time <= start_time:
        end_time = meta.duration_seconds

    # Validate range
    start_time = max(0.0, min(start_time, meta.duration_seconds))
    clip_duration = max(0.01, end_time - start_time)

    # Compute target timestamps
    num_frames = int(round(clip_duration * target_fps))
    num_frames = max(1, min(num_frames, max_frames))

    timestamps = [start_time + (i / target_fps) for i in range(num_frames)]
    # Ensure all timestamps are within video duration
    timestamps = [t for t in timestamps if t <= meta.duration_seconds + 0.05]

    # Calculate target dimensions
    scale_factor = max(0.1, min(scale_percent / 100.0, 1.0))
    target_width = max(16, int(round(meta.width * scale_factor)))
    target_height = max(16, int(round(meta.height * scale_factor)))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to read video file: {video_path}")

    extracted_frames: List[Image.Image] = []

    try:
        for t in timestamps:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            # Convert BGR (OpenCV) to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)

            # Resize if scaled
            if scale_percent != 100:
                pil_img = pil_img.resize(
                    (target_width, target_height),
                    resample=Image.Resampling.LANCZOS
                )

            extracted_frames.append(pil_img)

    finally:
        cap.release()

    if not extracted_frames:
        raise RuntimeError("No frames could be extracted from the specified video interval.")

    return extracted_frames
