from elements.data.predictor_parameters import PredictorParameters
from gradio_server.locker import Locker
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.params.param_settings import ParamSetting


class DynamicProcessingSetting(ParamSetting):
    """
    Changes whether the application corrects for slowing processing times by skipping frames. This can severely reduce the accuracy of the count as for all data gets used.
    Can be toggled in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters

    def update(self, dynamic_processing: bool):
        with self.locker.lock:
            self.logger.info(f"Changed dynamic processing bool from {str(self.general_settings.dynamic_processing)} to {str(dynamic_processing)}")
            self.general_settings.dynamic_processing = dynamic_processing
            self.predictor_parameters = None
