from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class ClassesSetting(ParamSetting):
    """
    Updated the expected classes coming from the predictions. Gets set on startup
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, classes: list):
        with self.locker.lock:
            self.logger.info(f"Changed classes value from {str(self.general_settings.classes)} to {str(classes)}")
            self.general_settings.classes = classes
