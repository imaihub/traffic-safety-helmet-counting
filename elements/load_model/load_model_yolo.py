import os

import torch.nn
from ultralytics import YOLO

from elements.load_model.load_model_base import LoadModel
from elements.utils import Logger

logger = Logger.setup_logger()


class LoadModelYolo(LoadModel):
    """
    This class is responsible for loading in yolov8 models.
    """
    def __init__(self, model_name: str, weights_file: str, num_classes: int = 1, device: str = "cuda", version: str = "n"):
        super().__init__(weights_file=weights_file, num_classes=num_classes, device=device)
        self.model_name = model_name
        self.version = version

    def load_model(self) -> torch.nn.Module:
        """
        Loads in a monolytics YOLO model and returns it
        """
        return YOLO(model=str(os.path.join(self.base_path, "models", "architectures", self.model_name, self.weights_file))).to(self.device)
