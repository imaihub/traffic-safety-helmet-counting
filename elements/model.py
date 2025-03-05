from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelConfig:
    """
    The object the fields of a model configuration gets wrapped in.
    """
    architecture: str
    weights: str
    normalize_type: Optional[str] = None
    version: Optional[str] = None
    input_width: Optional[int] = None
    input_height: Optional[int] = None
    task_type: Optional[str] = None
    classes: Optional[list[str]] = field(default_factory=list)
    load_model_type: Optional[str] = None
    box_threshold: Optional[float] = None
    bpp: int = 8
    mean: Optional[float] = None
    std: Optional[float] = None
    tracker: Optional[str] = None
