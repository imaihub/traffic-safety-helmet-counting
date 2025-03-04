from enum import Enum


class OutputType(Enum):
    IMAGE_DATA = 1
    JSON = 2

class Tasks(Enum):
    OBJECT_DETECTION=0
    CLASSIFICATION=1
    SEMANTIC_SEGMENTATION=2
    INSTANCE_SEGMENTATION=3
    TRACKING=4

class NormalizeType(Enum):
    """
    Method of normalization to be used in the preprocessing step
    """
    IMAGE_NET = 0
    SCALED_IMAGE_NET = 1
    YOLO = 2
    CUSTOM = 3

class InputMode(Enum):
    """
    Different modes of tracking, either video file input or camera feed input
    """
    CAMERA = 0
    FILE = 1

class ApplicationMode(Enum):
    """
    Mode of the application, either CLI or GUI
    """
    CLI = 0
    GUI = 1