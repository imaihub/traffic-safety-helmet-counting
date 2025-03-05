from elements.locker import Locker
from elements.settings.params.param_settings import ParamSetting


class TaskTypeSetting(ParamSetting):
    """
    Sets the task type mode. Gets set on startup only
    """
    def __init__(self, general_settings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings

    def update(self, task_type: str):
        with self.locker.lock:
            self.logger.info(f"Changed save type from {str(self.general_settings.task_type)} to {str(task_type)}")
            self.general_settings.task_type = task_type
