import numpy as np
import ultralytics

from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.utils import Logger


class Predictor:
    """
    A Predictor instance is responsible for performing inference on a given image with the model set in the constructor.
    """
    def __init__(self, model_settings: ModelSettings, general_settings: GeneralSettings):
        self.logger = Logger.setup_logger()
        self.model_settings = model_settings
        self.general_settings = general_settings

    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Performs inference on a given image.
        """
        if self.model_settings.model is None:
            return np.asarray([])
        if isinstance(self.model_settings.model, ultralytics.models.yolo.model.YOLO):
            predictions = self.model_settings.model(image, imgsz=image.shape[0], verbose=False, conf=self.general_settings.box_threshold, device=self.model_settings.device)
        else:
            predictions = self.model_settings.model(image)
        return predictions
