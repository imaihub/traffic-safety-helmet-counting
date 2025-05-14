from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class SaveNewObjects(ParamSetting):
    """
    Change the save new objects result setting. If on, saves a .png of the processed image if it contains new objects
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, save_new_objects: bool) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed save new objects from {str(self.general_settings.save_new_objects)} to {str(save_new_objects)}")
            self.general_settings.save_new_objects = save_new_objects
