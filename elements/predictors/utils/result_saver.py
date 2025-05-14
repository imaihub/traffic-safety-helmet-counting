import os
import shutil
import time

import cv2
import numpy as np

from elements.utils import Logger


class ResultSaver:
    """
    A ResultSaver instance is responsible for saving the results of a video analysis, whether that is loose images or the fully processed video.

    By using it as a context manager, you are sure that the VideoWriter instance gets released and that a copy of the resulting video gets saved
    """

    def __init__(self, output_folder: str):
        self.logger = Logger.setup_logger()
        self.local_output_folder = "output"
        self.output_folder = output_folder
        self.out_file: str = os.path.join(self.output_folder, "output", "videos", f"{time.time()}.mp4")
        self.out_video = None
        self.frame_size = None
        self.initialize_folder()

    def __enter__(self) -> 'ResultSaver':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if isinstance(self.out_video, cv2.VideoWriter):
            self.out_video.release()
            self.save_copy_video()

    def initialize_folder(self) -> None:
        """
        Create output folders if they do not exist already.
        """
        self.logger.info('Initializing folder')
        os.makedirs(os.path.join(self.local_output_folder, "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.output_folder, "output", "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.output_folder, "output", "images"), exist_ok=True)

    def save_image(self, image: np.ndarray) -> None:
        """
        Save an image to the output folder. Used when the count gets updated
        """
        self.logger.info(f"Saving image to {os.path.join(self.output_folder, 'output', 'images', f'{time.time()}.png')}")
        cv2.imwrite(filename=os.path.join(self.output_folder, "output", "images", f"{time.time()}.png"), img=image)

    def initiate_result_video(self, width: int, height: int, fps: float) -> None:
        """
        Instantiates a cv2.VideoWriter object
        """
        # Proper frame size and codec
        self.frame_size = (width, height)  # (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 files

        # Video writer
        self.out_video = cv2.VideoWriter(filename=self.out_file, fourcc=fourcc, fps=fps, frameSize=self.frame_size)

    def append_image_to_video(self, image: np.ndarray) -> None:
        """
        Appends an image to the cv2.VideoWriter instance created using initiate_result_video(...)
        """
        if not self.frame_size:
            self.logger.exception("No VideoWriter instance initiated yet, use initiate_result_video first.")
            return

        self.logger.info("Appending image to video")
        self.out_video.write(cv2.resize(image, self.frame_size))

    def save_copy_video(self) -> str:
        """
        Copies the fully analyzed video to a local directory
        """
        local_cache_copy = os.path.join(self.local_output_folder, "videos", os.path.basename(self.out_file))
        shutil.copy(src=self.out_file, dst=local_cache_copy)
        self.logger.info(f"Saving video to: {local_cache_copy}")
        return local_cache_copy
