import traceback

from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class InputWidthSetting(ParamSetting):
    """
    Changes the input width value which gets used in the preprocessing step.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, input_width: int) -> None:
        with self.locker.lock:
            self.logger.info(f"Changing input width from {str(self.general_settings.input_width)} to {str(input_width)}")
            try:
                assert int(input_width) > 0
                self.general_settings.input_width = int(input_width)
            except Exception as e:
                self.logger.error(traceback.format_exc())
                self.logger.exception(e)
                self.logger.info(f"Sticking with an input width of {self.general_settings.input_width}")