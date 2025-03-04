import torch

from elements.enums import NormalizeType
from elements.processing.base import Processing


class NormalizeImageNet(Processing):
    """
    Normalize an image using the basic ImageNet mean and std
    """

    def __init__(self, device: str = "cuda"):
        super().__init__()
        self.device = device
        self.mean = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32).view((3, 1, 1))
        self.std = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32).view((3, 1, 1))

    def apply(self, img: torch.Tensor):
        """
        Apply the normalization on the passed image
        """
        img -= self.mean.to(img.device)
        img /= self.std.to(img.device)

        return img


class DenormalizeImageNet(Processing):
    """
    Denormalize an image using the basic ImageNet mean and std
    """
    def __init__(self, ):
        super().__init__()
        self.mean = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32).view((3, 1, 1))
        self.std = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32).view((3, 1, 1))

    def apply(self, img: torch.Tensor):
        """
        Apply the denormalization on the passed image
        """
        img = (img * self.std.to(img.device)) + self.mean.to(img.device)

        return img
