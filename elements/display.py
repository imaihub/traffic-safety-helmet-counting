import cv2
import numpy as np


class Display:
    """
    This class enables functionality around visualizing numpy arrays with cv2.imshow
    """

    def __init__(self, window_name: str = "data"):
        self.window_name = window_name

    def show_image(self, image: np.ndarray) -> None:
        """
        Simply shows the image with cv2.imshow

        :param image: image to show
        """
        cv2.imshow(self.window_name, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        cv2.waitKey(1)

    def close(self) -> None:
        """
        Closes all windows
        """
        cv2.destroyAllWindows()
