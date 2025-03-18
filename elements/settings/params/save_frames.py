from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class SaveAllFrames(ParamSetting):
    """
    Change the save all frames setting. If on, every raw frame from the camera will be saved.
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, save_all_frames: bool) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed save all frames from {str(self.general_settings.save_all_frames)} to {str(save_all_frames)}")
            self.general_settings.save_all_frames = save_all_frames
