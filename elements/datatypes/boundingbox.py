from typing import Optional


class BoundingBox:
    """
    Representation of axis-aligned bounding boxes.
    """

    def __init__(self, class_id: int = -1, class_name: Optional[str] = None):
        self.track_id: Optional[int] = None
        self.x1: Optional[float] = None
        self.y1: Optional[float] = None
        self.x2: Optional[float] = None
        self.y2: Optional[float] = None
        self.class_id: int = class_id
        self.class_name: Optional[str] = class_name
        self.confidence: Optional[float] = None
        self._relative: bool = False

    @property
    def area(self) -> float:
        """Get the area of the bounding box."""
        return self.width * self.height if self.width and self.height else 0.0

    @property
    def width(self) -> float:
        """Get the width of the bounding box."""
        return self.x2 - self.x1 if self.x1 is not None and self.x2 is not None else 0.0

    @property
    def height(self) -> float:
        """Get the height of the bounding box."""
        return self.y2 - self.y1 if self.y1 is not None and self.y2 is not None else 0.0

    @property
    def x(self) -> Optional[float]:
        """Get the x-coordinate of the center."""
        return (self.x1 + self.x2) / 2 if self.x1 and self.x2 else None

    @property
    def y(self) -> Optional[float]:
        """Get the y-coordinate of the center."""
        return (self.y1 + self.y2) / 2 if self.y1 and self.y2 else None

    @property
    def relative(self) -> bool:
        """Check if coordinates are relative."""
        return self._relative

    def get_class_name(self, classes: list[str]) -> str:
        """Get the class name from a list of class names if not explicitly set."""
        return self.class_name or classes[self.class_id]

    def set_minmax_xy(self, xmin: float, ymin: float, xmax: float, ymax: float, relative: bool = False):
        """Set bounding box using min/max coordinates."""
        self.x1, self.y1, self.x2, self.y2 = float(xmin), float(ymin), float(xmax), float(ymax)
        self._relative = relative