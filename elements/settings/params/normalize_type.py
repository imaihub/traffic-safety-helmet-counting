from elements.enums import NormalizeType
from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class NormalizeTypeSetting(ParamSetting):
    """
    Changes the normalization method used in the preprocessing step.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, normalize_type: str) -> None:
        normalize_map = {NormalizeType.IMAGE_NET.name.lower(): NormalizeType.IMAGE_NET, NormalizeType.YOLO.name.lower(): NormalizeType.YOLO, NormalizeType.SCALED_IMAGE_NET.name.lower(): NormalizeType.SCALED_IMAGE_NET}

        with self.locker.lock:
            key = normalize_type.lower()
            if key in normalize_map:
                old_type = self.general_settings.normalize_type.name if self.general_settings.normalize_type else "None"
                new_type = normalize_map[key]
                self.general_settings.normalize_type = new_type
                self.logger.info(f"Changed normalize type from {old_type} to {new_type.name}")
            else:
                raise RuntimeError(f"Normalize type '{normalize_type}' does not exist, quitting.")
