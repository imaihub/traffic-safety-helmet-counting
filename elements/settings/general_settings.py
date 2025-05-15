import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from elements.enums import NormalizeType, InputMode, ApplicationMode


@dataclass
class GeneralSettings:
    """
    These are the parameters that get used throughout the application.
    """
    def __init__(self) -> None:
        self.task_type: Optional[str] = None
        self.mean: Optional[list] = None
        self.std: Optional[list] = None
        self.camera_mode: InputMode = InputMode.FILE
        self.application_mode: ApplicationMode = ApplicationMode.GUI
        self.tracked_classes: list = []
        self.classes: list = []
        self.bpp: int = 8
        self.gamma_correction_bool: bool = False
        self.gamma_correction_value: float = 2.2
        self.reset_stats_min: float = 0.0
        self.input_width: int = 0
        self.input_height: int = 0

        self.screen_width: int = 1920
        self.screen_height: int = 1080

        self.camera_index: int = -1

        self.save_all_frames: bool = False
        self.save_results: bool = False
        self.save_new_objects: bool = False

        self.normalize_type: Optional[NormalizeType] = None
        self.advanced_view: bool = False
        self.realistic_processing: bool = True
        self.box_threshold: float = 0.6
        self.output_folder: str = os.path.join(Path.home(), "Downloads")