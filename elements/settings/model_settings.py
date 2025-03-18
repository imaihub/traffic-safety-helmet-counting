from dataclasses import dataclass
from typing import Optional

import torch.nn


@dataclass
class ModelSettings:
    """
    Stored the model related settings. These are the parameters that actually get used in the application
    """

    def __init__(self) -> None:
        self.reset: bool = False
        self.model: Optional[torch.nn.Module] = None
        self.architecture: Optional[str] = None
        self.device: str = "cuda:0"
        self.weights_path: Optional[str] = None
