from typing import Iterator

import cv2
import numpy as np


class VideoReader:
    """
    A VideoReader instance is responsible for taking in a video path and returning it frame for frame in a generator method.
    """
    def __init__(self, input_path: str) -> None:
        self.vidcap: cv2.VideoCapture = cv2.VideoCapture(input_path)
        if not self.vidcap.isOpened():
            raise ValueError(f"Failed to open video file: {input_path}")
        self.total_frames: int = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps: float = self.vidcap.get(cv2.CAP_PROP_FPS)

    def __enter__(self) -> 'VideoReader':
        return self

    def frames(self, skip_frames: int = 0) -> Iterator[tuple[int, np.ndarray]]:
        current_frame: int = 0
        success, image = self.vidcap.read()
        while success:
            if current_frame >= skip_frames:
                yield current_frame, image
            current_frame += 1
            success, image = self.vidcap.read()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()

    def release(self) -> None:
        self.vidcap.release()
