import os
import time

import cv2


class VideoCapture:
    """
    A VideoCapture instance is responsible for reading images from the webcam and returning it frame for frame in a generator method.
    """

    def __init__(self, camera_index: int = 0, save_all_frames: bool = False, save_directory: str = "output",
                 camera_width: int = 1920, camera_height: int = 1080):
        self.vidcap = cv2.VideoCapture(camera_index, apiPreference=cv2.CAP_ANY, params=[
            cv2.CAP_PROP_FRAME_WIDTH, camera_width,
            cv2.CAP_PROP_FRAME_HEIGHT, camera_height
        ])
        self.save_all_frames = save_all_frames
        self.save_folder = os.path.join(save_directory, str(time.time()))
        if self.save_all_frames:
            os.makedirs(self.save_folder, exist_ok=True)

    def __enter__(self):
        return self

    def frames(self):
        success, image = self.vidcap.read()
        i = 0
        while success:
            yield image
            success, image = self.vidcap.read()
            if self.save_all_frames:
                cv2.imwrite(os.path.join(self.save_folder, f"frame{str(i)}.png"), image)
                i += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def release(self):
        self.vidcap.release()
