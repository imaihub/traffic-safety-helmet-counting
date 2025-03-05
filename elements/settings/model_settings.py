from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelSettings:
    """
    Stored the model related settings. These are the parameters that actually get used in the application
    """

    def __init__(self):
        self.model = None
        self.architecture: Optional[str] = None
        self.device: str = "cuda:0"
        self.weights_path: Optional[str] = None
