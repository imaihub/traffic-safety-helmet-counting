import threading


class Locker:
    """
    Simple wrapper that can get passed to different functions to safely perform actions.
    """
    def __init__(self) -> None:
        self.lock = threading.Lock()
