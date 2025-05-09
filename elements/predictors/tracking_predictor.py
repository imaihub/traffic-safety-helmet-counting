from functools import partial
from pathlib import Path
from typing import Optional, Union

import boxmot

from elements.display import Display
from elements.enums import InputMode
from elements.locker import Locker
from elements.predictors.camera import PredictorTrackerCamera
from elements.predictors.parameters import PredictorParameters
from elements.predictors.predictor_factory import PredictorFactory
from elements.predictors.video_input import PredictorTrackerInput
from elements.processing.postprocessing.models.yolo import decode_yolo_boxes_pt
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.tracking_settings import TrackingSettings
from elements.trackers.tracker_factory import TrackerFactory


class PredictTracking(PredictorFactory):
    def __init__(self,
                 general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 tracking_settings: Optional[TrackingSettings] = None,
                 websocket_server=None,
                 display: Optional[Display] = None,
                 input_path: Optional[Union[str, list]] = None,
                 skip_frames: Optional[int] = 0,
                 locker: Locker = None):
        super().__init__(general_settings=general_settings,
                         model_settings=model_settings,
                         tracking_settings=tracking_settings,
                         websocket_server=websocket_server,
                         display=display,
                         skip_frames=skip_frames,
                         input_path=input_path,
                         locker=locker)

    def get_predictor(self):
        tracker_generator = None
        if self.tracking_settings.tracker.casefold() == "deepocsort":
            tracker_generator = partial(boxmot.DeepOcSort,
                                        asso_func="centroid",
                                        half=False,
                                        reid_weights=Path("osnet_x1_0_msmt17.pt"),
                                        per_class=True)
        else:
            self.logger.exception(f"Unknown tracking case: {self.tracking_settings.tracker}")
            RuntimeError(f"Unknown tracking case: {self.tracking_settings.tracker}")

        self.tracking_settings.tracker_generator = tracker_generator

        _, tracker_processor = TrackerFactory.create(general_settings=self.general_settings,
                                                     tracking_settings=self.tracking_settings,
                                                     model_settings=self.model_settings)

        self.tracking_settings.reset = False

        predictor_parameters = PredictorParameters(result_processor=decode_yolo_boxes_pt,
                                                   tracker_processor=tracker_processor,
                                                   display=self.display,
                                                   skip_frames=self.skip_frames,
                                                   input_path=self.input_path)

        if self.general_settings.camera_mode == InputMode.CAMERA:
            predictor = PredictorTrackerCamera(
                general_settings=self.general_settings,
                model_settings=self.model_settings,
                tracking_settings=self.tracking_settings,
                predictor_parameters=predictor_parameters,
                websocket_server=self.websocket_server,
                locker=self.locker)
        else:
            predictor = PredictorTrackerInput(
                general_settings=self.general_settings,
                model_settings=self.model_settings,
                tracking_settings=self.tracking_settings,
                predictor_parameters=predictor_parameters,
                websocket_server=self.websocket_server,
                locker=self.locker)
        return predictor, predictor_parameters
