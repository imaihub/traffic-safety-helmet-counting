import contextlib

from elements.enums import Tasks, InputMode
from elements.load_model.load_model_yolo import LoadModelYolo
from elements.locker import Locker
from elements.predictors.parameters import PredictorParameters
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.params.param_settings import ParamSetting

import gradio as gr


class WeightsSetting(ParamSetting):
    """
    Changes the weights used for inference. Can be chosen in the GUI
    """

    def __init__(self, general_settings: GeneralSettings, model_settings: ModelSettings, config_parser, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.model_settings = model_settings
        self.config_parser = config_parser
        self.predictor_parameters = predictor_parameters

    def update(self, weights_path: str):
        """
        This function loads in the weights to a model. It dynamically searches int the folders with the name of the architecture and looks of the weights_file which is the name of the weights file.

        :param weights_path: the name of the weights file
        """
        with self.locker.lock if not (self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold() and self.general_settings.camera_mode == InputMode.CAMERA) else contextlib.nullcontext():
            self.config_parser.update_current_config()

            self.logger.info(f"Changed weights from {str(self.model_settings.weights_path)} to {str(weights_path)}")
            if weights_path is not self.model_settings.weights_path and weights_path:
                if self.config_parser.current_config.load_model_type in ["yolo"]:
                    self.general_settings.classes = self.config_parser.current_config.classes
                    self.model_settings.model = LoadModelYolo(weights_file=weights_path, model_name=self.model_settings.architecture, version=self.config_parser.current_config.version).load_model()
            self.model_settings.weights_path = weights_path
            self.general_settings.tracked_classes = []
            self.predictor_parameters = None
        return gr.CheckboxGroup(label="Which objects should be tracked", choices=self.config_parser.current_config.classes, value=self.general_settings.tracked_classes, interactive=True)
