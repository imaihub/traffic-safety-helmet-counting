from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class ResetStatsMinSetting(ParamSetting):
    """
    Changes the interval the stats should be reset using camera mode
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, minutes: int) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed reset stats min from {str(self.general_settings.reset_stats_min)} to {str(minutes)}")
            self.general_settings.reset_stats_min = minutes
