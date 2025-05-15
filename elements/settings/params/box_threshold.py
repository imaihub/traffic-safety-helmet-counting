from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class BoxThresholdSetting(ParamSetting):
    """
    Changes the box threshold when a user changes the text field.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, box_threshold: float) -> None:
        with self.locker.lock:
            try:
                if not 0.0 < float(box_threshold) < 1.0:  # Skip update
                    return
                self.logger.info(f"Changed box_threshold value from {str(self.general_settings.box_threshold)} to {str(box_threshold)}")
                self.general_settings.box_threshold = float(box_threshold)
            except Exception as e:
                self.logger.exception(e)
                self.general_settings.box_threshold = 0.
