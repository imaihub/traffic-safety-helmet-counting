import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from elements.enums import NormalizeType, InputMode, ApplicationMode


@dataclass
class GeneralSettings:
    """
    These are the parameters that get used throughout the application. They initially get set using the current config from the config.yaml
    """
    def __init__(self):
        super().__init__()
        self.task_type: Optional[str] = None
        self.mean: Optional[list] = None
        self.std: Optional[list] = None
        self.camera_mode: InputMode = InputMode.FILE
        self.application_mode = ApplicationMode.GUI
        self.tracked_classes = Optional[list]
        self.classes: list = []
        self.bpp: int = 8
        self.gamma_correction_bool: bool = False
        self.gamma_value: float = 2.2
        self.input_width: int = 0
        self.input_height: int = 0
        self.normalize_type: Optional[NormalizeType] = None
        self.advanced_view: bool = False
        self.realistic_processing: bool = True
        self.box_threshold: float = 0.6
        self.output_folder: str = os.path.join(Path.home(), "Downloads")