from dataclasses import dataclass


@dataclass
class TrackingSettings:
    """
    This dataclass stores all tracker parameters that got chosen in the GUI
    """
    def __init__(self):
        super().__init__()
        self.tracker = None
        self.reset = False
        self.param_options = {"HIGH_TRACKING_THRESHOLD": "", "LOW_TRACKING_THRESHOLD": "", "MATCHING_THRESHOLD": "", "TRACKING_BUFFER": "",
                              "MAXIMUM_DISTANCE": "", "MAXIMUM_IOU_DISTANCE": "", "MAXIMUM_AGE": "",
                              "DETECTION_THRESHOLD": "", "MAXIMUM_HITS": ""}

        self.current_options = {0: "HIGH_TRACKING_THRESHOLD", 1: "LOW_TRACKING_THRESHOLD", 2: "MATCHING_THRESHOLD", 3: "TRACKING_BUFFER"}

