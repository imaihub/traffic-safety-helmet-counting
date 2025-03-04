import torch

from elements.enums import NormalizeType
from elements.processing.base import Processing


class NormalizeCustom(Processing):
    """
    Normalize an image using custom mean and std values
    """

    def __init__(self, mean: list = None, std: list = None):
        super().__init__()
        self.mean = torch.tensor(mean, dtype=torch.float32).view(3, 1, 1)
        self.std = torch.tensor(std, dtype=torch.float32).view(3, 1, 1)

    def apply(self, img: torch.Tensor):
        """
        Apply the normalization on the passed image
        """
        img -= self.mean.to(img.device)
        img /= self.std.to(img.device)

        return img


class DenormalizeCustom(Processing):
    """
    Denormalize an image using custom mean and std values
    """

    def __init__(self, mean: list = None, std: list = None):
        super().__init__()
        self.mean = torch.tensor(mean, dtype=torch.float32).view(3, 1, 1)
        self.std = torch.tensor(std, dtype=torch.float32).view(3, 1, 1)

    def apply(self, img: torch.Tensor):
        """
        Apply the denormalization on the passed image
        """
        img = (img * self.std.to(img.device)) + self.mean.to(img.device)

        return img
