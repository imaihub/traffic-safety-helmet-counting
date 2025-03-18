import time
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional

import cv2
import numpy as np
import pybase64
import torch

from elements.display import Display
from elements.enums import ApplicationMode
from elements.locker import Locker
from elements.predictors.parameters import PredictorParameters
from elements.predictors.utils.box_processor import BoxProcessor
from elements.predictors.utils.predictor import Predictor
from elements.predictors.utils.result_saver import ResultSaver
from elements.processing.postprocessing.object_detection.combine_boxes import CombineBoxes
from elements.processing.preprocessing.resize import Resize
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.tracking_settings import TrackingSettings
from elements.trackers.tracker_factory import TrackerFactory
from elements.utils import Logger, get_color_map
from gradio_server.websocket_manager.websocket_manager import WebSocketServer


class PredictorBase(ABC):
    """
    PredictorBase contains already defined functions and functions that still have to be implemented regarding the inference on camera feeds and video input files.
    """

    def __init__(self,
                 general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 tracking_settings: TrackingSettings,
                 predictor_parameters: PredictorParameters,
                 websocket_server: WebSocketServer):
        self.logger = Logger.setup_logger()
        self.websocket = websocket_server

        self.general_settings = general_settings
        self.model_settings = model_settings
        self.tracking_settings = tracking_settings

        self.color_map = get_color_map(self.general_settings.classes)

        self.aborting = None
        self.predictor_parameters = predictor_parameters

        self.predictor, self.box_processor, self.result_saver, self.combine_boxes = self.initialize_helpers()

    def initialize_helpers(self) -> tuple[Predictor, BoxProcessor, ResultSaver, CombineBoxes]:
        """
        Instantiate building blocks for the prediction process and postprocessing like Predictor, BoxProcessor, ResultSaver and CombineBoxes
        """
        result_saver = self.initialize_result_saver()

        box_processor = self.initialize_box_processor()
        predictor = self.initialize_predictor()
        combine_boxes = self.initialize_combine_boxes()

        return predictor, box_processor, result_saver, combine_boxes

    def initialize_predictor(self) -> Predictor:
        """
        Instantiate the predictor from the general settings and model settings
        """
        return Predictor(model_settings=self.model_settings, general_settings=self.general_settings)

    def initialize_box_processor(self) -> BoxProcessor:
        """
        Instantiate the box processor from the general settings and model settings
        """
        return BoxProcessor(general_settings=self.general_settings)

    def initialize_result_saver(self) -> ResultSaver:
        """
        Instantiate the result saver from general settings and model settings
        """
        return ResultSaver(output_folder=self.general_settings.output_folder)

    def initialize_combine_boxes(self) -> CombineBoxes:
        """
        Instantiate the combine_boxes from the general settings and model settings
        """
        return CombineBoxes(general_settings=self.general_settings, color_map=self.color_map)

    def update_settings(self) -> None:
        """
        Resets the tracker
        """
        _, tracker_processor = TrackerFactory.create(general_settings=self.general_settings,
                                                     tracking_settings=self.tracking_settings)
        self.predictor_parameters.tracker_processor = tracker_processor

        self.box_processor = self.initialize_box_processor()
        self.predictor = self.initialize_predictor()
        self.combine_boxes = self.initialize_combine_boxes()

        self.tracking_settings.reset = False

    def abort(self) -> None:
        """
        Stops the analyzing, invoked by user interactions with the GUI
        """
        self.aborting = True

    def wait_for_websocket(self) -> None:
        """
        Wait until websocket connection is established
        """
        self.logger.info("Waiting for websocket connection...")
        while not self.websocket.client_connected_event.is_set():
            self.logger.info("Waiting 1 second for websocket connection")
            time.sleep(1)
        self.logger.info("Websocket connecting established")

    def set_response(self, image: np.ndarray) -> None:
        """
        Set the base64 representation of the image as a response in the websocket instance
        """
        _, buffer = cv2.imencode('.jpg', image,
                                 params=[int(cv2.IMWRITE_JPEG_QUALITY), 85])  # Convert the frame to JPG format

        frame_base64 = pybase64.b64encode(buffer).decode('utf-8')  # Encode to base64

        if self.general_settings.application_mode == ApplicationMode.GUI:
            self.websocket.set_response(response=frame_base64)

    def process_frame(self, image: np.ndarray, display: Optional[Display]) -> tuple[np.ndarray, bool]:
        """
        Performs inference on a single image using the predictor passed. Additionally does:
        1. Creates a numpy representations of the boxes from the model
        2. Updates the tracker state with those boxes
        3. Visualizes the boxes on top of the original image
        4. Display the resulting image if a Display instance is passed
        """
        visualization_image = deepcopy(image)

        image = cv2.resize(src=image, dsize=(int(self.general_settings.input_width), int(self.general_settings.input_height)))

        predictions = self.predictor.predict(image=image)
        boxes_numpy = self.box_processor.extract_boxes(predictions=predictions)

        try:
            active_boxes = self.predictor_parameters.tracker_processor.update_boxes(boxes=boxes_numpy, image=image)
        except Exception as e:
            self.logger.error(e)
            active_boxes = []

        boxes_from_active_tracks = self.predictor_parameters.tracker_processor.get_boxes_from_active_tracks(active_tracks=active_boxes)
        save_image = self.predictor_parameters.tracker_processor.update_tracks(active_tracks=boxes_from_active_tracks, verbose=False)

        visualization_image = cv2.resize(visualization_image, (self.general_settings.screen_width, self.general_settings.screen_height))
        boxes_from_active_tracks = Resize.resize_boxes(boxes=boxes_from_active_tracks,
                                                       dimension_from=(int(self.general_settings.input_width), int(self.general_settings.input_height)),
                                                       dimension_to=(int(self.general_settings.screen_width), int(self.general_settings.screen_height)))

        if boxes_from_active_tracks:
            self.combine_boxes.set_boxes(boxes=boxes_from_active_tracks)
            visualization_image = self.combine_boxes.apply(image=visualization_image)

        visualization_image = self.predictor_parameters.tracker_processor.update_count(image=visualization_image)

        if display is not None:
            display.show_image(cv2.cvtColor(visualization_image, cv2.COLOR_BGR2RGB))

        return visualization_image, save_image

    @torch.no_grad()
    @abstractmethod
    def predict(self, locker: Locker) -> Optional[np.ndarray]:
        """
        Abstract function for handling a camera feed and video input files for inference
        """
        pass
