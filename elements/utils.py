import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

import cv2
import numpy as np


def get_color_map(classes: list, color_map_style: int = cv2.COLORMAP_SPRING) -> list:
    """
    Generate a color mapping where the class_ids gets matched with a specific color.
    """
    color_map = np.expand_dims(np.arange(len(classes)), 1)
    color_map = ((color_map / len(classes)) * 255).astype(np.uint8)
    color_map = cv2.applyColorMap(np.ascontiguousarray(color_map), color_map_style)
    return list(color_map)


def get_optimal_font_scale(text: str, width: float) -> float:
    for scale in reversed(range(0, 60, 1)):
        text_size = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale / 10, thickness=1)
        new_width = text_size[0][0]
        if new_width <= width:
            print(new_width)
            return scale / 10
    return 1


class Logger:
    """
    Provides a logger for informative print statements and saves them for further investigation.
    """
    _logger = None

    @staticmethod
    def setup_logger() -> logging.Logger:
        if Logger._logger is None:
            Logger._logger = logging.getLogger()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            os.makedirs(os.path.join("logs", ), exist_ok=True)

            file_handler = RotatingFileHandler(
                os.path.join(
                    "logs",
                    f"{str(datetime.datetime.now()).replace('-', '_').replace(':', '_')}.log",
                ),
                mode="a",
                maxBytes=10 * 1024 * 1024,
                backupCount=2,
                encoding="utf-8",
                delay=False,
            )
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            Logger._logger.setLevel(logging.INFO)
            Logger._logger.addHandler(file_handler)
            Logger._logger.addHandler(console_handler)
        return Logger._logger
