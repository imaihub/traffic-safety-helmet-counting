import torch

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

    def apply(self, image: torch.Tensor):
        """
        Apply the normalization on the passed image
        """
        image -= self.mean.to(image.device)
        image /= self.std.to(image.device)

        return image


class DenormalizeImageNet(Processing):
    """
    Denormalize an image using the basic ImageNet mean and std
    """

    def __init__(self):
        super().__init__()
        self.mean = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32).view((3, 1, 1))
        self.std = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32).view((3, 1, 1))

    def apply(self, image: torch.Tensor):
        """
        Apply the denormalization on the passed image
        """
        image = (image * self.std.to(image.device)) + self.mean.to(image.device)

        return image
