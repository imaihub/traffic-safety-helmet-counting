import multiprocessing
import time
from typing import Optional, Self

import torch

from elements.utils import Logger


class Timer:
    """
    This class gives the developer the option to easily time their code. Use it like a context manager.
    """

    def __init__(
            self,
            name: str,
            include_gpu: Optional[bool] = False,
            wait_time: Optional[int] = None,  # In milliseconds
            print_time: Optional[bool] = False,
            include_cpu_time: Optional[bool] = False,
    ):
        self.logger = Logger.setup_logger()

        self.name = name
        self.wait_time = wait_time
        self.include_gpu = include_gpu
        self.print_time_bool = print_time
        self.start_real: float = 0
        self.start_cpu: float = 0
        self.end_real: float = 0
        self.end_cpu: float = 0
        self.include_cpu_time = include_cpu_time

    def __enter__(self) -> Self:
        """
        Entering function of the ContextManager
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exiting function of the ContextManager
        """

        self.stop()

        if self.print_time_bool:
            self.print_time(include_cpu_time=self.include_cpu_time)

        if self.wait_time:
            self.wait_until()

    def start(self) -> None:
        """
        Start the timer
        """
        if self.include_gpu:
            if multiprocessing.parent_process() is None and torch.cuda.is_available():
                torch.cuda.synchronize()

        self.start_real = time.perf_counter()
        self.start_cpu = time.process_time()

    def stop(self) -> None:
        """
        Stop the timer
        """
        if self.include_gpu and torch.cuda.is_available():
            torch.cuda.synchronize()

        self.end_real = time.perf_counter()
        self.end_cpu = time.process_time()

    def elapsed_real_time(self) -> float:
        """
        Calculated the time, should only be called after calling stop()
        """
        if self.end_real is None:
            self.stop()
        return self.end_real - self.start_real

    def print_time(self, include_cpu_time: bool = False) -> None:
        """
        Prints the time of the code
        """
        real_time = self.elapsed_real_time()
        self.logger.info(f"Real time for {self.name}: {real_time:.4f} seconds")
        if include_cpu_time:
            cpu_time = self.end_cpu - self.start_cpu
            self.logger.info(f"CPU time for {self.name}: {cpu_time:.4f} seconds")

    def reset(self) -> None:
        """
        Resets the timer
        """
        self.start_real = None
        self.start_cpu = None

    def wait_until(self) -> None:
        """
        Wait until a certain amount of milliseconds is passed from the moment the timer started
        """
        if self.wait_time is None:
            self.logger.warning("Wait time never set, thus cannot wait until a specific time")

        # Convert wait_time from milliseconds to seconds
        wait_time_seconds = self.wait_time / 1000

        current_difference = time.perf_counter() - self.start_real

        if current_difference < wait_time_seconds:
            remaining_time = wait_time_seconds - current_difference
            self.logger.info(f"Waiting for an additional {remaining_time:.4f} seconds")
            time.sleep(remaining_time)

    def get_timings(self) -> dict:
        """
        Get timing data for both real_time and cpu_time
        """
        return {
            "real_time": self.elapsed_real_time(),
            "cpu_time": self.end_cpu - self.start_cpu,
        }
