from elements.locker import Locker
from elements.settings.model_settings import ModelSettings
from elements.settings.params.param_settings import ParamSetting


class DeviceSetting(ParamSetting):
    """
    Changes the device used for inference.
    """
    def __init__(self, model_settings: ModelSettings, locker: Locker):
        super().__init__(locker)
        self.model_settings = model_settings

    def update(self, device: str) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed device from {str(self.model_settings.device)} to {str(device)}")
            if device is not self.model_settings.device:
                if self.model_settings.model is not None:
                    self.model_settings.model.to(device)
                self.model_settings.device = device
