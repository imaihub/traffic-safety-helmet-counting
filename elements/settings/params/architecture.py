from elements.enums import Tasks
from elements.locker import Locker
from elements.settings.params.param_settings import ParamSetting

import gradio as gr


class ArchitectureSetting(ParamSetting):
    """
    Changes the architecture when a user picks another from the DropDown element. Updates the available weight options when that happens
    """

    def __init__(self, general_settings, predictor_parameters, model_settings, config_parser, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.model_settings = model_settings
        self.predictor_parameters = predictor_parameters
        self.config_parser = config_parser

    def update(self, architecture: str) -> tuple:
        """
        Loads in the model given the architecture name. Some models need the weights to be loaded thus with those, nothing gets loaded in this function.

        return gr.DropDown component as the selectable weights list needs the architecture to find compatible weights
        """

        with self.locker.lock:
            self.logger.info(f"Changed architecture from {str(self.model_settings.architecture)} to {str(architecture)}")
            try:
                architecture = architecture.lower()
                self.model_settings.architecture = architecture
                self.general_settings.tracked_classes = []
                self.predictor_parameters = None
            except Exception as e:
                self.logger.exception(e)

        self.general_settings.input_width = self.config_parser.current_config.input_width
        self.general_settings.input_height = self.config_parser.current_config.input_height

        if self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold():
            return (gr.Dropdown(choices=[config.weights for config in self.config_parser.all_configs if config.architecture == architecture], interactive=True),
                    gr.Text(self.general_settings.input_width if self.general_settings.input_width else 0, interactive=True),
                    gr.Text(self.general_settings.input_height if self.general_settings.input_height else 0, interactive=True),
                    gr.CheckboxGroup(label="Which objects should be tracked", choices=self.config_parser.current_config.classes, value=self.general_settings.tracked_classes, interactive=True))
        else:
            return (gr.Dropdown(choices=[config.weights for config in self.config_parser.all_configs if config.architecture == architecture], interactive=True),
                    gr.Text(self.general_settings.input_width if self.general_settings.input_width else 0, interactive=True),
                    gr.Text(self.general_settings.input_height if self.general_settings.input_height else 0, interactive=True))
