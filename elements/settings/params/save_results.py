from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class SaveResults(ParamSetting):
    """
    Change the save result setting. If on, every processed frame.
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, save_results: bool) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed save results from {str(self.general_settings.save_results)} to {str(save_results)}")
            self.general_settings.save_results = save_results
