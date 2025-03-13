from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class CameraDimensionSetting(ParamSetting):
    """
    Changes the width and height of the expected camera output.
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, width: int, height: int):
        with self.locker.lock:
            self.logger.info(f"Changed camera dimensions from {str(self.general_settings.camera_width)}x{str(self.general_settings.camera_height)} "
                             f"to {width}x{height}")
            self.general_settings.camera_width = width
            self.general_settings.camera_height = height


class CameraIndexSetting(ParamSetting):
    """
    Changes camera based on the camera index..
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, index: int):
        with self.locker.lock:
            self.logger.info(f"Changed camera index from {str(self.general_settings.camera_index)} "
                             f"to {str(index)}")
            self.general_settings.camera_index = index