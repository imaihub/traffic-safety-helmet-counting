from abc import ABC, abstractmethod
from typing import Optional, Union, List

from elements.display import Display
from elements.utils import Logger
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.model_settings import ModelSettings
from gradio_server.settings.tracking_settings import TrackingSettings
from gradio_server.websocket_manager.websocket_manager_upload import WebSocketServerUpload


class PredictorFactory(ABC):
    """
    Base class of every factory constructing a Predictor object
    """
    def __init__(self, general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 tracking_settings: Optional[TrackingSettings],
                 websocket_server: Optional[WebSocketServerUpload],
                 display: Optional[Display],
                 skip_frames: Optional[int],
                 input_path: Optional[Union[str, List]]):
        self.logger = Logger.setup_logger()

        self.general_settings = general_settings
        self.tracking_settings = tracking_settings
        self.model_settings = model_settings
        self.websocket_server = websocket_server
        self.display = display
        self.skip_frames = skip_frames
        self.input_path = input_path

    @abstractmethod
    def get_predictor(self):
        pass
