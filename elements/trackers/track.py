class Track:
    """
    Custom track object.
    """
    def __init__(self, xyxy: list, id: int, cls: int, confidence: float):
        self.xyxy = xyxy
        self.id = id
        self.cls = cls
        self.confidence = confidence
