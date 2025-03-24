from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class BoxThresholdSetting(ParamSetting):
    """
    Changes the box threshold when a user changes the text field. Tries to parse the string to float before setting it internally to prevent errors
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, box_threshold: float) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed box_threshold value from {str(self.general_settings.box_threshold)} to {str(box_threshold)}")
            try:
                self.general_settings.box_threshold = float(box_threshold)
            except Exception as e:
                self.logger.exception(e)
                self.general_settings.box_threshold = 0.
