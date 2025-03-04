import numpy as np
import torch.nn
import ultralytics


class Predictor:
    """
    A Predictor instance is responsible for performing inference on a given image with the model set in the constructor. Depending on the model, it can give extra parameters for example.
    """
    def __init__(self, model: torch.nn.Module, box_threshold: float):
        self.model = model
        self.box_threshold = box_threshold

    def predict(self, image: np.ndarray):
        """
        Performs inference on a given image
        """
        if isinstance(self.model, ultralytics.models.yolo.model.YOLO):
            predictions = self.model(image, verbose=True, conf=self.box_threshold)
        else:
            predictions = self.model(image)
        return predictions
