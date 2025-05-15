from dataclasses import dataclass


@dataclass
class TrackingSettings:
    """
    This dataclass stores all tracker parameters that got chosen in the GUI.
    """
    def __init__(self) -> None:
        self.tracker = None
        self.reset: bool = False
        self.tracker_generator = None
        self.param_options: dict = {"HIGH_TRACKING_THRESHOLD": "", "LOW_TRACKING_THRESHOLD": "", "MATCHING_THRESHOLD": "", "TRACKING_BUFFER": "", "MAXIMUM_DISTANCE": "", "MAXIMUM_IOU_DISTANCE": "", "MAXIMUM_AGE": "", "MAXIMUM_HITS": ""}

        self.current_options: dict = {0: "HIGH_TRACKING_THRESHOLD", 1: "LOW_TRACKING_THRESHOLD", 2: "MATCHING_THRESHOLD", 3: "TRACKING_BUFFER"}
