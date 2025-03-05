from elements.predictors.parameters import PredictorParameters
from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class RealisticProcessingSetting(ParamSetting):
    """
    Changes whether the application corrects for slowing processing times by skipping frames. This can severely reduce the accuracy of the count as for all data gets used.
    Can be toggled in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters

    def update(self, realistic_processing: bool):
        with self.locker.lock:
            self.logger.info(f"Changed dynamic processing bool from {str(self.general_settings.realistic_processing)} to {str(realistic_processing)}")
            self.general_settings.realistic_processing = realistic_processing
            self.predictor_parameters = None
