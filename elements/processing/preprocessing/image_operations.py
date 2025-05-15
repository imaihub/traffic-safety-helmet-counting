import base64
import io

import cv2
import numpy as np


class ImageOperations:
    @staticmethod
    def load_image(input_path: str, bit: int) -> np.ndarray:
        """
        Load an image from a path and return a numpy array representation.
        """
        if isinstance(input_path, str):
            input_data = cv2.imread(input_path, -1)
        else:
            input_data = base64.b64decode(input_path.split(",")[1])
            input_data = io.BytesIO(input_data)

        input_data = cv2.cvtColor(input_data, cv2.COLOR_BGR2RGB)

        if not bit:
            bit = 8
        else:
            bit = int(bit)
        if bit == 12:
            input_data = input_data.astype(np.int16)

        return input_data
