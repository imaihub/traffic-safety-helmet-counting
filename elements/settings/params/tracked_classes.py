from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class TrackedClassesSetting(ParamSetting):
    """
    Changes the tracked classes. Can be chosen in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, classes: list):
        with self.locker.lock:
            self.general_settings.tracked_classes = classes

