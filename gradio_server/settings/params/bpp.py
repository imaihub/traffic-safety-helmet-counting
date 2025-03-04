from elements.data.predictor_parameters import PredictorParameters
from gradio_server.locker import Locker
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.params.param_settings import ParamSetting


class BPPSetting(ParamSetting):
    """
    Changes the expect bit per pixel when a user changes the value using the DropDown menu
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, bpp: int):
        with self.locker.lock:
            self.logger.info(f"Changed bpp from {str(self.general_settings.bpp)} to {str(bpp)}")
            self.general_settings.bpp = bpp
