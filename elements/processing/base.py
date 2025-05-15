from abc import abstractmethod
from typing import Protocol, Union

import numpy as np
import torch


class Processing(Protocol):
    """
    Every class having the method apply with img as param is an instance of Processing.

    Every Processing instance should be a pre- or postprocessing step

    """
    @abstractmethod
    def apply(self, image: Union[np.ndarray, torch.Tensor]) -> Union[np.ndarray, torch.Tensor]:
        pass
