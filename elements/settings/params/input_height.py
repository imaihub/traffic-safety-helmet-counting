from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class InputHeightSetting(ParamSetting):
    """
    Changes the input height value which gets used in the preprocessing step. Can cause issues with inference. Can be changed in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, input_height: int) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed input height from {str(self.general_settings.input_height)} to {str(input_height)}")
            self.general_settings.input_width = int(input_height)
