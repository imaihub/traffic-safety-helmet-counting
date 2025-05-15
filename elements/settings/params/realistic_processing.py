from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class RealisticProcessingSetting(ParamSetting):
    """
    Changes whether the application corrects for too fast processing if using good hardware.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, realistic_processing: bool) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed dynamic processing bool from {str(self.general_settings.realistic_processing)} to {str(realistic_processing)}")
            self.general_settings.realistic_processing = realistic_processing
