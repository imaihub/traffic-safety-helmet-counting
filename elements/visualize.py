import cv2
import numpy as np


def draw_fps_text(image: np.ndarray, text: str, text_color: tuple = (40, 255, 255)):
    """
    Draws an FPS component on the image in the upper left corner.

    :param image: The image to draw on.
    :param text: Text to display above the progress bar.
    :param text_color: BGR color for the text.
    :return: Image with progress bar drawn on it.

    """
    img = image.copy()

    # Text position (above bar)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = 50
    text_y = 50

    # Draw text
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)

    return img


def draw_progress_bar(image: np.ndarray, text: str, percentage: float, bar_color: tuple = (0, 255, 0), bg_color: tuple = (50, 50, 50), text_color: tuple = (255, 255, 255)):
    """
    Draws a progress bar on the image with a label above it.

    :param image: The image to draw on.
    :param text: Text to display above the progress bar.
    :param percentage: Progress percentage (0 to 100).
    :param bar_color: BGR color of the progress fill.
    :param bg_color: BGR background color of the progress bar.
    :param text_color: BGR color for the text.
    :return: Image with progress bar drawn on it.

    """
    img = image.copy()
    h, w = img.shape[:2]

    # Progress bar dimensions
    bar_width = int(0.7 * w)
    bar_height = int(0.05 * h)
    bar_x = 50
    bar_y = int(h - bar_height - int(0.05 * h))  # Slight padding from bottom

    # Text position (above bar)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = int(bar_x + (bar_width / 2) - (text_size[0] / 2))
    text_y = bar_y - 10  # 10px padding above bar

    # Draw background bar
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), bg_color, -1)

    # Draw filled progress portion
    progress_width = int((percentage / 100.0) * bar_width)
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), bar_color, -1)

    # Draw text
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)

    return img
