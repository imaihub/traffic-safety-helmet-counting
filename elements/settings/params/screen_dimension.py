from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class ScreenDimensionSetting(ParamSetting):
    """
    Changes the width and height of the output result that will be displayed on the screen.
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, width: int, height: int) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed screen dimensions from {str(self.general_settings.screen_width)}x{str(self.general_settings.screen_height)} "
                             f"to {width}x{height}")
            self.general_settings.screen_width = width
            self.general_settings.screen_height = height
