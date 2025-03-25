from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting

class CameraIndexSetting(ParamSetting):
    """
    Changes camera based on the camera index.
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, index: str) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed camera index from {str(self.general_settings.camera_index)} to {str(index)}")
            self.general_settings.camera_index = int(index)
