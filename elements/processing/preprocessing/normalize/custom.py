import torch

from elements.processing.base import Processing


class NormalizeCustom(Processing):
    """
    Normalize an image using custom mean and std values
    """

    def __init__(self, mean: list = None, std: list = None):
        super().__init__()
        self.mean = torch.tensor(mean, dtype=torch.float32).view(3, 1, 1)
        self.std = torch.tensor(std, dtype=torch.float32).view(3, 1, 1)

    def apply(self, image: torch.Tensor):
        """
        Apply the normalization on the passed image
        """
        image -= self.mean.to(image.device)
        image /= self.std.to(image.device)

        return image


class DenormalizeCustom(Processing):
    """
    Denormalize an image using custom mean and std values
    """

    def __init__(self, mean: list = None, std: list = None):
        super().__init__()
        self.mean = torch.tensor(mean, dtype=torch.float32).view(3, 1, 1)
        self.std = torch.tensor(std, dtype=torch.float32).view(3, 1, 1)

    def apply(self, image: torch.Tensor):
        """
        Apply the denormalization on the passed image
        """
        image = (image * self.std.to(image.device)) + self.mean.to(image.device)

        return image
