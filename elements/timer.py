import time
import torch
from typing import Optional
from elements.utils import Logger
import multiprocessing


class Timer:
    """
    This class gives the developer the option to easily time their code. Use it like a context manager.
    """

    def __init__(
            self,
            name: str,
            include_gpu: Optional[bool] = False,
            wait_time: Optional[int] = None,
            print_timings: Optional[bool] = False,
    ):
        self.logger = Logger.setup_logger()

        self.name = name
        self.wait_time = wait_time
        self.include_gpu = include_gpu
        self.print_timings = print_timings
        self.start_real = None
        self.start_cpu = None
        self.end_real = None
        self.end_cpu = None

    def __enter__(self):
        """
        Entering function of the ContextManager
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exiting function of the ContextManager
        """

        self.stop()

        if self.print_timings:
            self.print_times()

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

    def print_times(self) -> None:
        """
        Prints the time of the code
        """
        real_time = self.elapsed_real_time()
        cpu_time = self.end_cpu - self.start_cpu
        self.logger.info(f"Real time for {self.name}: {real_time:.4f} seconds")
        # self.logger.info(f"CPU time for {self.name}: {cpu_time:.4f} seconds")

    def reset(self) -> None:
        """
        Resets the timer
        """
        self.start()

    def wait_until(self) -> None:
        """
        Wait until a certain amount of milliseconds is passed from the moment the timer started
        """
        if self.wait_time is None:
            self.logger.info("Wait time never set, thus can not wait forever")

        current_difference = time.perf_counter() - self.start_real

        if current_difference < self.wait_time:
            time.sleep(self.wait_time - current_difference)

    def get_timings(self) -> dict:
        """
        Get timing data for both real_time and cpu_time
        """
        return {
            "real_time": self.elapsed_real_time(),
            "cpu_time": self.end_cpu - self.start_cpu,
        }
