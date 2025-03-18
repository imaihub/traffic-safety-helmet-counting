from typing import Union

import numpy as np

from elements.datatypes.boundingbox import BoundingBox


class Resize:
    @staticmethod
    def resize_boxes(boxes: list[Union[BoundingBox, np.ndarray]], dimension_from: tuple[int, int], dimension_to: tuple[int, int]) -> list[Union[BoundingBox, np.ndarray]]:
        width_ratio = dimension_to[0] / dimension_from[0]
        height_ratio = dimension_to[1] / dimension_from[1]

        for i in range(len(boxes)):
            box = boxes[i]
            if isinstance(box, BoundingBox):
                box.set_minmax_xy(
                    xmin=box.x1 * width_ratio,
                    ymin=box.y1 * height_ratio,
                    xmax=box.x2 * width_ratio,
                    ymax=box.y2 * height_ratio
                )
            elif isinstance(box, np.ndarray):
                box[0] = box[0] * width_ratio
                box[1] = box[1] * height_ratio
                box[2] = box[2] * width_ratio
                box[3] = box[3] * height_ratio
        return boxes
