from abc import ABC, abstractmethod

from elements.utils import Logger
from elements.locker import Locker


class ParamSetting(ABC):
    """
    Base class for all settings
    """
    def __init__(self, locker: Locker):
        self.locker = locker
        self.logger = Logger.setup_logger()

    @abstractmethod
    def update(self, **params):
        pass












