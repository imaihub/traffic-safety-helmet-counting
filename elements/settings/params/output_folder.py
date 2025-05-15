from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting


class OutputFolderSetting(ParamSetting):
    """
    Changes output folder where the final video and interim images get stored.
    """
    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, output_folder: str) -> None:
        with self.locker.lock:
            self.logger.info(f"Changed output folder from {str(self.general_settings.output_folder)} to {str(output_folder)}")
            self.general_settings.output_folder = output_folder
