from typing import Union, Optional

import cv2
import numpy as np

from elements.datatypes.boundingbox import BoundingBox


class Resize:
    def __init__(self, height_to: int, width_to: int, width_from: Optional[int] = None, height_from: Optional[int] = None):
        self.width_from, self.height_from, self.width_ratio, self.height_ratio = None, None, None, None
        self.dimensions_set = False
        self.height_to = height_to
        self.width_to = width_to

        if width_from and height_from:
            self.set_dimensions(width_from, height_from)

    def set_dimensions(self, width_from: int, height_from: int):
        self.width_from = width_from
        self.height_from = height_from
        self.width_ratio = self.width_to / width_from
        self.height_ratio = self.height_to / height_from
        self.dimensions_set = True

    def resize_image(self, image: np.ndarray):
        image = cv2.resize(image, (self.width_to, self.height_to))
        return image

    def resize_boxes(self, boxes: list[Union[BoundingBox, np.ndarray]]) -> list[Union[BoundingBox, np.ndarray]]:
        for i in range(len(boxes)):
            if isinstance(boxes[i], BoundingBox):
                boxes[i].set_minmax_xy(xmin=boxes[i].x1 * self.width_ratio, ymin=boxes[i].y1 * self.height_ratio, xmax=boxes[i].x2 * self.width_ratio, ymax=boxes[i].y2 * self.height_ratio)
            elif isinstance(boxes[i], np.ndarray):
                boxes[i][0] = boxes[i][0] * self.width_ratio
                boxes[i][1] = boxes[i][1] * self.height_ratio
                boxes[i][2] = boxes[i][2] * self.width_ratio
                boxes[i][3] = boxes[i][3] * self.height_ratio
        return boxes


