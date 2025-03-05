import time
from abc import ABC, abstractmethod
from typing import Optional

import cv2
import numpy as np
import pybase64
import torch

from elements.display import Display
from elements.enums import ApplicationMode
from elements.settings.model_settings import ModelSettings
from elements.predictors.parameters import PredictorParameters
from elements.predictors.utils.box_processor import BoxProcessor
from elements.predictors.utils.predictor import Predictor
from elements.predictors.utils.result_saver import ResultSaver
from elements.processing.postprocessing.object_detection.combine_boxes import CombineBoxes
from elements.settings.general_settings import GeneralSettings
from elements.utils import Logger, get_color_map


class PredictorBase(ABC):
    """
    PredictorBase contains already defined functions and functions that still have to be implemented regarding the inference on camera feeds and video input files.
    """

    def __init__(self,
                 model: torch.nn.Module,
                 general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 predictor_parameters: PredictorParameters,
                 websocket_server):
        self.logger = Logger.setup_logger()
        self.websocket = websocket_server

        self.general_settings = general_settings
        self.model_settings = model_settings
        self.model = model

        self.color_map = get_color_map(self.general_settings.classes)

        self.aborting = None
        self.predictor_parameters = predictor_parameters

        self.initialize_helpers()

    def initialize_helpers(self):
        """
        Instantiate building blocks for the prediction process and postprocessing like Predictor, BoxProcessor, ResultSaver and CombineBoxes
        """
        self.predictor = Predictor(self.model, self.general_settings.box_threshold)
        self.box_processor = BoxProcessor(tracker_processor=self.predictor_parameters.tracker_processor,
                                          tracked_classes=self.general_settings.tracked_classes,
                                          classes=self.general_settings.classes,
                                          box_threshold=self.general_settings.box_threshold)

        self.result_saver = ResultSaver(output_folder=self.general_settings.output_folder)
        self.combine_boxes = CombineBoxes(classes=self.general_settings.classes, color_map=self.color_map)

    def update_model(self, model: torch.nn.Module):
        """
        Dynamically change model. Can be used during analyzing on users discretion
        """
        self.model = None
        self.logger.info("Updating model")
        self.model = model
        self.logger.info("Updated model")

    def abort(self):
        """
        Stops the analyzing, invoked by user interactions with the GUI
        """
        self.aborting = True

    def wait_for_websocket(self):
        """
        Wait until websocket connection is established
        """
        self.logger.info("Waiting for websocket connection...")
        while not self.websocket.client_connected_event.is_set():
            self.logger.info("Waiting 1 second for websocket connection")
            time.sleep(1)
        self.logger.info("Websocket connecting established")

    def set_response(self, image: np.ndarray):
        """
        Set the base64 representation of the image as a response in the websocket instance
        """
        _, buffer = cv2.imencode('.jpg', image, params=[int(cv2.IMWRITE_JPEG_QUALITY), 85])  # Convert the frame to JPG format

        frame_base64 = pybase64.b64encode(buffer).decode('utf-8')  # Encode to base64

        if self.general_settings.application_mode == ApplicationMode.GUI:
            self.websocket.set_response(response=frame_base64)

    def process_frame(self, image: np.ndarray, display: Optional[Display]):
        """
        Performs inference on a single image using the predictor passed. Additionally does:
        1. Creates a numpy representations of the boxes from the model
        2. Updates the tracker state with those boxes
        3. Visualizes the boxes on top of the original image
        4. Display the resulting image if a Display instance is passed
        """
        predictions = self.predictor.predict(image=image)
        boxes_numpy = self.box_processor.extract_boxes(predictions=predictions)

        active_boxes = self.box_processor.tracker_processor.update_boxes(boxes=boxes_numpy, image=image)
        boxes_from_active_tracks = self.box_processor.tracker_processor.get_boxes_from_active_tracks(active_tracks=active_boxes)
        save_image = self.box_processor.tracker_processor.update_tracks(active_tracks=boxes_from_active_tracks, verbose=False)

        if boxes_from_active_tracks:
            self.combine_boxes.set_boxes(boxes=boxes_from_active_tracks)
            image = self.combine_boxes.apply(image=image)

        image = self.box_processor.tracker_processor.update_count(image=image)

        if display is not None:
            display.show_image(cv2.cvtColor(cv2.resize(src=image, dsize=(1920, 1080)), cv2.COLOR_BGR2RGB))

        return image, save_image

    @torch.no_grad()
    @abstractmethod
    def predict(self, input_path: str, display: Optional[Display], skip_frames: int = 0):
        """
        Abstract function for handling a camera feed and video input files for inference
        """
        pass
