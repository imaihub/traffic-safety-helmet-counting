from dataclasses import dataclass
from typing import Optional, Callable, List, Union

from elements.display import Display
from elements.trackers.tracker import Tracker

@dataclass(frozen=True)
class PredictorParameters:
    """
    This class consists of fields that are necessary for the processing of the images by the predictor.
    """
    result_processor: Callable
    tracker_processor: Tracker
    display: Optional[Display] = None
    skip_frames: Optional[int] = 0
    input_path: Optional[Union[str, List]] = None
