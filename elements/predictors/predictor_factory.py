from abc import ABC, abstractmethod
from typing import Optional, Union, List

from elements.display import Display
from elements.locker import Locker
from elements.predictors.base_predictor import PredictorBase
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.tracking_settings import TrackingSettings
from elements.utils import Logger


class PredictorFactory(ABC):
    """
    Base class of every factory constructing a Predictor object
    """
    def __init__(self, general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 tracking_settings: Optional[TrackingSettings],
                 websocket_server,
                 display: Optional[Display],
                 skip_frames: Optional[int],
                 input_path: Optional[Union[str, List]],
                 locker: Locker):
        self.logger = Logger.setup_logger()

        self.general_settings = general_settings
        self.tracking_settings = tracking_settings
        self.model_settings = model_settings
        self.websocket_server = websocket_server
        self.display = display
        self.skip_frames = skip_frames
        self.input_path = input_path
        self.locker = locker

    @abstractmethod
    def get_predictor(self) -> PredictorBase:
        pass
