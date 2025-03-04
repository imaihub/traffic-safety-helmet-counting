from elements.enums import OutputType
from gradio_server.locker import Locker
from gradio_server.settings.params.param_settings import ParamSetting


class OutputTypeSetting(ParamSetting):
    """
    Changes the output type setting. Gets set during startup depending on the argument given.
    """
    def __init__(self, general_settings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, output_type: OutputType):
        with self.locker.lock:
            self.logger.info(f"Changed output type {str(self.general_settings.output_type.name)} to {str(output_type.name)}")
            self.general_settings.output_type = output_type
