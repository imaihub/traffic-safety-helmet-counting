from elements.enums import InputMode
from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class CameraModeSetting(ParamSetting):
    """
    Sets the mode of this application.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, camera_mode: InputMode) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed camera mode from {str(self.general_settings.camera_mode.name)} to {str(camera_mode.name)}")
            self.general_settings.camera_mode = camera_mode
