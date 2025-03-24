import cv2
import numpy as np


class Display:
    """
    This class enables functionality around visualizing numpy arrays with cv2.imshow
    """

    def __init__(self, window_name: str = "data") -> None:
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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
