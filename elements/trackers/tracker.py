from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List

import cv2
import numpy as np

from elements.datatypes.boundingbox import BoundingBox
from elements.utils import Logger, get_color_map
from gradio_server.settings.general_settings import GeneralSettings


class Tracker(ABC):
    """
    Custom Tracker classes acting as an interface to the BoxMot tracker objects. Includes methods regarding updating and showing count info
    """

    def __init__(self, general_settings: GeneralSettings, min_hits: int, tracker):
        self.count = 0
        self.min_hits = min_hits
        self.tracker = tracker
        self.logger = Logger.setup_logger()
        self.general_settings = general_settings
        self.tracks: dict = {}
        self.counts: dict = {k: 0 for k in self.general_settings.classes}
        self.color_map = get_color_map(self.general_settings.classes)

    def reset(self):
        """
        Resets the count of the tracker
        """
        self.logger.info("Resetting tracker")
        self.count = 0
        self.counts = {k: 0 for k in self.general_settings.classes}

    @abstractmethod
    def update_tracks(self, image, detections) -> bool:
        """
        updates info on the tracks, including whether this track has already passed the line where it increments the count of a class
        """
        pass

    def update_boxes(self, boxes: List, image: np.ndarray) -> list[np.ndarray]:
        """
        Passes the detections to the BoxMot tracker object so it can look whether they belong to an existing track of a new one
        """
        tracker_tracks = sum(self.tracker.per_class_active_tracks.values(), [])
        new_potential_active_tracks = self.tracker.update(np.asarray(boxes), image)
        active_tracks = []
        for potential_active_track in new_potential_active_tracks:
            for track in tracker_tracks:
                if track.age > self.min_hits and track.id == int(potential_active_track[4]):
                    active_tracks.append(potential_active_track)
                    break

        return active_tracks

    def update_count(self, img: np.ndarray) -> np.ndarray:
        """
        Pastes the classes and counts on the image with dynamic font size and thickness.
        """
        scale = 1

        # Calculate dynamic fontscale and thickness
        image_height, image_width = img.shape[:2]
        base_font_size = 1  # Base font size for reference
        fontscale = int((image_width / image_height * base_font_size)) * scale
        thickness = max(1, int(min(image_width, image_height) / 400))  # Ensure thickness is at least 1

        text = self.get_formatted_count()
        img = deepcopy(img)
        y = int(image_height / 1.05)  # Start Y position for text placement

        for t in text.split("\n"):
            class_name = t.split(":")[0]
            if class_name == "":
                continue

            # Get color for the class
            color_index = self.general_settings.classes.index(class_name)
            text_color = tuple(int(v) for v in self.color_map[color_index][0])

            # Put text on the image
            x = int(image_width / 1.2)  # X position for text placement
            cv2.putText(img, t, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontscale, text_color, thickness)

            # Update Y position for next line
            y -= int(50 * (fontscale / (base_font_size / scale)))  # Adjust line spacing based on fontscale

        return img

    def get_formatted_count(self):
        """
        Formats the class and counts in a string to show on the image
        """
        text = ""
        for c in self.counts.keys():
            if c in self.general_settings.tracked_classes:
                text += f"{str(c)}: {self.counts[c]}\n"
        return text

    def get_boxes_from_active_tracks(self, active_tracks: list):
        """
        Returns a list of bounding boxes created from info inside active_tracks, a list of
        """
        bboxes = []
        for track in active_tracks:
            b_new = BoundingBox(class_id=int(track[6]))
            b_new.set_minmax_xy(float(track[0]), float(track[1]), float(track[2]), float(track[3]))
            b_new.confidence = float(track[5])
            b_new.track_id = track[4]
            bboxes.append(b_new)
        return bboxes
