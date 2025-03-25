import os
import time
from typing import Self, Iterator

import cv2
import numpy as np

from elements.settings.general_settings import GeneralSettings
from elements.utils import Logger

logger = Logger.setup_logger()

# Common resolutions to try
possible_resolutions = {
    (640, 480): False,
    (1024, 768): False,
    (1280, 720): False,
    (1920, 1080): False,
}

def get_webcam_settings(camera_index: int = -1, verbose: bool = False) -> cv2.VideoCapture | None:
    """
    Tests webcam settings automatically to get valid settings, namely the camera index and maximum valid resolution.

    :param camera_index: if manually set, this is the camera index to use. -1 means automatic
    :param verbose: give a summary of possible webcam settings

    :return: camera index to use, and the maximum valid resolution.
    """
    def create_video_capture(camera_index: int, resolution: tuple) -> cv2.VideoCapture:
        cap = cv2.VideoCapture(camera_index, apiPreference=cv2.CAP_ANY)

        # Force MJPG (compressed, supports higher res)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        return cap

    cap = None
    maximum_resolution = None

    # Check whether user input camera index is valid
    if camera_index >= 0:
        cap = cv2.VideoCapture(camera_index)

        ok, frame = cap.read()
        if not ok:
            logger.exception(f"Camera index {camera_index} is not a valid camera index.")
            return None

    if camera_index < 0:
        # Determine usable camera index first
        for i in range(4):
            cap = cv2.VideoCapture(i)

            ok, frame = cap.read()
            if not ok:
                continue

            camera_index = i

    if camera_index < 0:
        raise ValueError("No valid camera index found, camera mode not possible")

    # Loop over possible resolutions to check which is valid
    for resolution in possible_resolutions.keys():
        if isinstance(cap, cv2.VideoCapture):
            cap.release()

        cap = create_video_capture(camera_index, resolution)

        ok, frame = cap.read()
        if ok and frame.shape[:2] == resolution[::-1]:
            possible_resolutions[resolution] = True
            maximum_resolution = resolution
            continue

    if maximum_resolution is None:
        logger.exception("No valid resolution found, camera mode not possible")
        return None


    if verbose:
        print("Possible webcam settings:")
        for resolution in possible_resolutions:
            print(f"Resolution: {resolution}: {'Yes' if possible_resolutions[resolution] else 'No'}")

    if cap is not None:
        cap.release()

    cap = create_video_capture(camera_index, maximum_resolution)

    return cap



class VideoCapture:
    """
    A VideoCapture instance is responsible for reading images from the webcam and returning it frame for frame in a generator method.
    """

    def __init__(self, camera_index: int = 0, save_directory: str = "output"):
        self.logger = Logger.setup_logger()
        self.vidcap = get_webcam_settings(camera_index=camera_index, verbose=True)
        self.save_folder = os.path.join(save_directory, str(time.time()))
        os.makedirs(self.save_folder, exist_ok=True)

    def __enter__(self) -> Self:
        return self

    def frames(self, general_settings: GeneralSettings) -> Iterator[np.ndarray]:
        success, image = self.vidcap.read()
        i: int = 0
        while success:
            yield image
            success, image = self.vidcap.read()
            if general_settings.save_all_frames:
                logger.info(f"Saving frame to {os.path.join(self.save_folder, f'frame{str(i)}.png')}")
                cv2.imwrite(os.path.join(self.save_folder, f"frame{str(i)}.png"), image)
                i += 1
        return None

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()

    def release(self) -> None:
        if isinstance(self.vidcap, cv2.VideoCapture):
            self.vidcap.release()
