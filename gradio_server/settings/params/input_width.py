from elements.data.predictor_parameters import PredictorParameters
from gradio_server.locker import Locker
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.params.param_settings import ParamSetting


class InputWidthSetting(ParamSetting):
    """
    Changes the input width value which gets used in the preprocessing step. Can cause issues with inference. Can be changed in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters

    def update(self, input_width: int):
        with self.locker.lock:
            self.logger.info(f"Changed input width from {str(self.general_settings.input_width)} to {str(input_width)}")
            self.general_settings.input_width = int(input_width)
            self.predictor_parameters = None
