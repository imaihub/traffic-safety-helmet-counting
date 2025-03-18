import sys
from abc import abstractmethod, ABC

import torch.nn

from elements.utils import Logger


class LoadModel(ABC):
    """
    Base class for loading in models with an abstract load_model returning the instance of the model
    """

    def __init__(self, weights_file: str, num_classes: int = 1, device: str = "cuda"):
        self.logger = Logger.setup_logger()
        self.base_path = getattr(sys, '_MEIPASS', "")
        self.weights_file = weights_file
        self.device = device
        self.num_classes = num_classes

    @abstractmethod
    def load_model(self) -> torch.nn.Module:
        """
        Function loading in and returning the instance of the model. Required to be implemented
        """
        pass
