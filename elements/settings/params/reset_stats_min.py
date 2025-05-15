import traceback

from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class ResetStatsMinSetting(ParamSetting):
    """
    Changes the interval the stats should be reset using camera mode.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, minutes: int) -> None:
        with self.locker.lock:
            self.logger.info(f"Changing reset stats min from {str(self.general_settings.reset_stats_min)} to {str(minutes)}")
            try:
                assert int(minutes) > 0
                self.general_settings.reset_stats_min = int(minutes)
            except Exception as e:
                self.logger.error(traceback.format_exc())
                self.logger.exception(e)
                self.logger.info(f"Sticking with an reset stats minutes of {self.general_settings.reset_stats_min}")
