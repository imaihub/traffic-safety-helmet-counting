from abc import ABC

from elements.locker import Locker
from elements.utils import Logger


class ParamSetting(ABC):
    """
    Base class for all settings.
    """
    def __init__(self, locker: Locker):
        self.locker = locker
        self.logger = Logger.setup_logger()
