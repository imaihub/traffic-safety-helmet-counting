import glob
import os
from typing import Iterator

import cv2
import numpy as np

from elements.enums import InputMode
from elements.utils import Logger


class FolderReader:
    def __init__(self, files: list[str]):
        self.files = files
        self.total_frames = len(files)
        self.fps: float = 30  # Default for image folders

    def __iter__(self) -> Iterator[tuple[int, np.ndarray]]:
        return self.frames()

    def frames(self, skip_frames: int = 0) -> Iterator[tuple[int, np.ndarray]]:
        for idx, file_path in enumerate(self.files):
            if idx < skip_frames:
                continue
            image = cv2.imread(file_path)
            if image is None:
                continue  # Skip unreadable images
            yield idx, image

    def release(self):
        pass


class VideoReader:
    """
    A VideoReader instance is responsible for taking in a video path and returning it frame for frame in a generator method.
    """
    def __init__(self, input_path: str, input_mode: InputMode) -> None:
        self.logger = Logger.setup_logger()
        self.input_mode = input_mode
        if self.input_mode == InputMode.IMAGES:
            files = glob.glob(os.path.join(input_path, "*.jpg"), recursive=True)
            files.extend(glob.glob(os.path.join(input_path, "*.JPG"), recursive=True))
            files.extend(glob.glob(os.path.join(input_path, "*.jpeg"), recursive=True))
            files.extend(glob.glob(os.path.join(input_path, "*.JPEG"), recursive=True))
            files.extend(glob.glob(os.path.join(input_path, "*.png"), recursive=True))
            files.extend(glob.glob(os.path.join(input_path, "*.PNG"), recursive=True))
            files = sorted(files)
            self.reader = FolderReader(files=files)
            self.total_frames = len(files)
            self.fps: float = 30 # Guess for FPS captured images without metadata
        else:
            try:
                self.reader = cv2.VideoCapture(input_path) # Works for both video files and RTSP streams
                if not self.reader.isOpened():
                    raise ValueError(f"Failed to open video file: {input_path}")
                self.total_frames: int = int(self.reader.get(cv2.CAP_PROP_FRAME_COUNT))
                self.fps: float = self.reader.get(cv2.CAP_PROP_FPS)
            except cv2.error:
                self.logger.exception(f"Failed to open video file: {input_path}", exc_info=True)
                raise ValueError(f"Failed to open video file: {input_path}")

    def __enter__(self) -> 'VideoReader':
        return self

    def frames(self, skip_frames: int = 0) -> Iterator[tuple[int, np.ndarray]]:
        if self.input_mode == InputMode.IMAGES:
            yield from self.reader.frames(skip_frames)
        else:
            current_frame = 0
            success, image = self.reader.read()
            while success:
                if current_frame >= skip_frames:
                    yield current_frame, image
                current_frame += 1
                success, image = self.reader.read()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()

    def release(self) -> None:
        self.reader.release()
