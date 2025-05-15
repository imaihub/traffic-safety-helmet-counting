from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class InputHeightSetting(ParamSetting):
    """
    Changes the input height value which gets used in the preprocessing step.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, input_height: int) -> None:
        with self.locker.lock:
            self.logger.info(f"Changing input height from {str(self.general_settings.input_height)} to {str(input_height)}")
            try:
                assert int(input_height) > 0
                self.general_settings.input_height = int(input_height)
            except Exception as e:
                self.logger.exception(e)
                self.logger.info(f"Sticking with an input height of {self.general_settings.input_height}")
