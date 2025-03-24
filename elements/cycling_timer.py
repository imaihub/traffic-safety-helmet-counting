import threading
import time
from datetime import datetime, timedelta
from typing import Callable

from elements.utils import Logger


class CyclingTimer:
    """
    This class provides functionality to keep track of a long timer and execute some code after that time has elapsed. Automatically resets.
    """

    def __init__(
            self,
            name: str,
            minutes: float,
            fn: Callable,
            lock: threading.Lock,
    ):
        self.logger = Logger.setup_logger()

        self.finish: bool = False
        self.name = name
        self.minutes = minutes
        self.fn = fn
        self.lock = lock
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None

    def start(self) -> None:
        """
        Start the timer
        """
        self.logger.info(f"Starting {self.name} timer to reset every {self.minutes} minutes")

        while not self.finish:
            self.start_time = datetime.now()
            self.end_time = datetime.now() + timedelta(minutes=self.minutes)

            while datetime.now() < self.end_time:
                time.sleep(self.minutes)

            with self.lock:
                self.fn()

    def stop(self):
        """
        Stop the timer by setting the finish flag
        """
        self.finish = True

    def reset(self) -> None:
        """
        Resets the timer
        """
        self.start()

    def get_time_left(self) -> tuple[float, float]:
        """
        Calculates the time left in seconds and returns that amount including the percentage of progress.
        """
        elapsed_seconds = (datetime.now() - self.start_time).total_seconds()
        return round((self.minutes * 60) - elapsed_seconds, 1), 100 - (elapsed_seconds / (self.minutes * 60) * 100)
