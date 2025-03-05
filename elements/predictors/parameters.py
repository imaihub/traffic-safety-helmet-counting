from dataclasses import dataclass
from typing import Optional, Callable, List, Union

from elements.display import Display
from elements.trackers.tracker_processor import TrackerProcessor


@dataclass(frozen=True)
class PredictorParameters:
    """
    This class consists of fields that are necessary for the processing of the images by the predictor.
    """
    result_processor: Callable
    tracker_processor: TrackerProcessor
    skip_frames: int = 0
    display: Optional[Display] = None
    input_path: Optional[Union[str, List]] = None
