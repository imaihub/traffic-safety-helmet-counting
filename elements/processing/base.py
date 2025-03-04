from abc import abstractmethod
from typing import Protocol

import torch

from elements.utils import Logger


class Processing(Protocol):
    """
    Every class having the method apply with img as param is an instance of Processing. Every Processing instance should be a pre- or postprocessing step
    """
    def __init__(self):
        self.logger = Logger.setup_logger()

    @abstractmethod
    def apply(self, img: torch.Tensor):
        pass
