from typing import Optional

import cv2
import numpy as np

from elements.datatypes.boundingbox import BoundingBox
from elements.processing.base import Processing
from elements.settings.general_settings import GeneralSettings
from elements.utils import get_color_map, Logger


class CombineBoxes(Processing):
    """
    Merges bounding boxes into an image.
    """
    def __init__(self, general_settings: GeneralSettings, color_map: Optional[list], ratios: Optional[tuple] = None):
        self.logger = Logger.setup_logger()
        self.general_settings = general_settings
        self.boxes: list[BoundingBox] = []
        self.color_map: list = get_color_map(classes=general_settings.classes) if color_map is None else color_map
        self.ratios = ratios

    def set_boxes(self, boxes: list[BoundingBox]) -> None:
        """
        Sets the boxes to visualize.
        """
        self.boxes = boxes

    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Visualizes the boxes set in set_boxes with the confidence, class name and track id.
        """
        if not self.general_settings.bpp == 8:
            for v in self.color_map:
                v /= (2**8 - 1)
                v * (2**self.general_settings.bpp - 1)

        if len(self.boxes) == 0:
            self.logger.warning(f"No boxes found")
            return image

        # Display the boxes given the first threshold value
        for i, box in enumerate(self.boxes):
            if not self.general_settings.classes[int(box.class_id)] in self.general_settings.tracked_classes:
                continue

            x1, x2 = round(box.x1), round(box.x2)
            y1, y2 = round(box.y1), round(box.y2)
            if self.ratios is not None:
                x1, x2 = x1 * self.ratios[0], x2 * self.ratios[0]
                y1, y2 = y1 * self.ratios[1], y2 * self.ratios[1]

            text_position = (x1 + 10, y1 + 60)

            image = np.ascontiguousarray(image)
            color = tuple([int(v) for v in tuple(self.color_map[int(box.class_id)][0])])

            # Draw rectangle
            image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 4)
            cv2.putText(img=image, text=f"{str(round(box.confidence, 2))} {self.general_settings.classes[int(box.class_id)]} id: {int(box.track_id)}", org=text_position, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=color, thickness=2)

        return image
