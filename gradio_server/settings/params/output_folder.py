from gradio_server.locker import Locker
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.model_settings import ModelSettings
from gradio_server.settings.params.param_settings import ParamSetting


class OutputFolderSetting(ParamSetting):
    """
    Changes output folder where the final video and interim images get stored. Can be changed in the GUI
    """

    def __init__(self, general_settings: GeneralSettings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, output_folder: str):
        with self.locker.lock:
            self.logger.info(f"Changed output folder from {str(self.general_settings.output_folder)} to {str(output_folder)}")
            self.general_settings.output_folder = output_folder
