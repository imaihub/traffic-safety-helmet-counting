from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class GammaCorrectionBoolSetting(ParamSetting):
    """
    Changes whether a gamma correction gets applied to the data for visualization purposes. Can be toggled in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker) -> None:
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, gamma_correction_bool: bool) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed gamma correction bool from {str(self.general_settings.gamma_correction_bool)} to {str(gamma_correction_bool)}")
            self.general_settings.gamma_correction_bool = gamma_correction_bool

class GammaCorrectionValueSetting(ParamSetting):
    """
    Changes the gamma value which gets used for the correction. Can be changed in the GUI
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker) -> None:
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, gamma_correction_value: float) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed gamma correction value from {str(self.general_settings.gamma_correction_value)} to {str(gamma_correction_value)}")
            self.general_settings.gamma_correction_value = gamma_correction_value