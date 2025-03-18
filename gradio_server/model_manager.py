import threading
import traceback
from typing import Union, List, Optional

import gradio as gr
import torch

from config.config_parser import ConfigParser
from elements.display import Display
from elements.enums import Tasks, InputMode
from elements.locker import Locker
from elements.predictors.base_predictor import PredictorBase
from elements.predictors.parameters import PredictorParameters
from elements.predictors.tracking_predictor import PredictTracking
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.tracking_settings import TrackingSettings
from elements.utils import Logger
from gradio_server.websocket_manager.websocket_manager import WebSocketServer

logger = Logger().setup_logger()


class ModelManager:
    """
    The middle man in this application. Holds objects required to predict, can abort tasks, reset the tracker stats and holds the logic to start he websocket server
    """

    general_settings: GeneralSettings
    model_settings: ModelSettings
    tracking_settings: TrackingSettings

    def __init__(self, args):
        self.args = args

        self.logger = Logger.setup_logger()
        self.locker = Locker()

        self.template = args.template
        self.config_parser = ConfigParser(template=self.template)

        self.predictor: Optional[PredictorBase] = None
        self.websocket_server: Optional[WebSocketServer] = None
        self.predictor_parameters: Optional[PredictorParameters] = None
        self.analysis_thread: Optional[threading.Thread] = None

        self.analyzing: bool = False

        self.images_boxes: list = []

    def initialize_settings(self, model_settings: ModelSettings, general_settings: GeneralSettings,
                            tracking_settings: TrackingSettings) -> None:
        """
        Simply sets the setting objects to the passed ones
        """
        self.tracking_settings = tracking_settings
        self.general_settings = general_settings
        self.model_settings = model_settings

    def get_parsed_config(self) -> ConfigParser:
        """
        Getter for the object holding the config info
        """
        return self.config_parser

    def start_websocket_server(self):
        """
        If the task type is tracking, start the websocket server
        """
        if self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold():
            self.websocket_server = WebSocketServer()
            self.websocket_server.run_websocket_server()

    def toggle_analysis(self) -> list[gr.Button]:
        """
        Start and turn off the camera feed analysis. Saves resulting video on quitting. Can also cancel current video analyses
        """
        self.reset_tracker()

        if self.general_settings.camera_mode == InputMode.CAMERA:
            if self.analyzing:
                self.analyzing = False
                self.predictor.abort()
                return [gr.Button(interactive=True, value="Start camera analysis"),
                        gr.Button(interactive=True, value="Reset tracker stats", visible=False)]
            else:
                self.analyzing = True
                self.analysis_thread = threading.Thread(target=self.predict, args=(None,))
                self.analysis_thread.start()
                return [gr.Button(interactive=True, value="Stop camera analysis"),
                        gr.Button(interactive=True, value="Reset tracker stats", visible=True)]
        else:
            self.predictor.abort()
            return [gr.Button(interactive=True, value="Cancel processing"),
                    gr.Button(interactive=True, value="Reset tracker stats", visible=True)]

    def switch_camera_mode(self) -> list[gr.Component]:
        """
        Changes the mode of the application, updates GUI accordingly
        """
        if self.general_settings.camera_mode == InputMode.FILE:
            self.general_settings.camera_mode = InputMode.CAMERA
            return [gr.Button(value="Set to file mode", interactive=True),
                    gr.File(label="Input video", elem_id="video_in", visible=False),
                    gr.Button(value="Start camera analysis", visible=True),
                    gr.Button(interactive=True, value="Reset tracker stats", visible=False)]

        else:
            self.general_settings.camera_mode = InputMode.FILE
            return [gr.Button(value="Set to camera input mode", interactive=True),
                    gr.File(label="Input video", elem_id="video_in", visible=True),
                    gr.Button(value="Cancel processing", visible=False),
                    gr.Button(interactive=True, value="Reset tracker stats", visible=False)]

    def await_analysis(self) -> list[Union[gr.Component, None]]:
        self.analysis_thread.join()
        analysis_button = gr.Button(interactive=True, value="Start camera analysis", visible=False)
        reset_tracker_stats_button = gr.Button(interactive=True, value="Reset tracker stats", visible=False)
        return [gr.update(value=None, interactive=True), analysis_button, reset_tracker_stats_button]

    def reset_tracker(self):
        """
        Resets the tracker including statistics
        """
        self.tracking_settings.reset = True

    def predict_gui(self, input_path: Union[str, List]):
        """
        Wrapper function to start the real predict function in a thread and return the required blocks. This way the processing does not freeze the application
        """
        self.analysis_thread = threading.Thread(target=self.predict, args=(input_path,))
        self.analysis_thread.start()
        return [gr.Button(interactive=True, value="Cancel processing", visible=True),
                gr.Button(interactive=True, value="Reset tracker stats", visible=True)]

    def check_model_settings(self):
        if not self.model_settings.architecture or not self.model_settings.weights_path:
            self.logger.warning("Input present but no model, tracker or weights")
            gr.Warning("Input present but no model, tracker or weights")
            return None
        return True


    @torch.no_grad()
    def predict(self, input_path: Optional[Union[str, list]], display: Optional[Display] = None, skip_frames: Optional[int] = 0):
        """
        Standard predict function called by the Gradio component. The supported tasks include: object detection and segmentation and tracking. Tracking uses a different Predictor class to process the images

        :param display: instance of Display to show results of each prediction locally
        :param input_path: path to an image or video
        :param skip_frames: amount of frames to skip in the case of processing a video file. Useful for debugging
        """
        if not self.check_model_settings():
            return None

        if self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold():
            self.predictor, self.predictor_parameters = PredictTracking(general_settings=self.general_settings,
                                                                        model_settings=self.model_settings,
                                                                        tracking_settings=self.tracking_settings,
                                                                        websocket_server=self.websocket_server,
                                                                        display=display,
                                                                        skip_frames=skip_frames,
                                                                        input_path=input_path).get_predictor()
        else:
            logger.exception("Task types other than tracking are not supported")
            gr.Warning("Task types other than tracking are not supported")
            return None

        try:
            result = self.predictor.predict(locker=self.locker)

        except Exception as e:
            if self.locker.lock.locked():
                self.locker.lock.release()
            logger.exception(e)
            logger.error(traceback.format_exc())
            return None

        return result
