from elements.enums import InputMode
from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class InputModeSetting(ParamSetting):
    """
    Sets the mode of this application.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, input_mode: InputMode) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed input mode from {str(self.general_settings.input_mode.name)} to {str(input_mode.name)}")
            self.general_settings.input_mode = input_mode
