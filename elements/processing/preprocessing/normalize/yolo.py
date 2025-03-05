import torch

from elements.processing.base import Processing


class NormalizeYolo(Processing):
    """
    Normalize an image by scaling the pixel values between 0 and 1
    """

    def __init__(self):
        super().__init__()

    def apply(self, image: torch.Tensor):
        """
        Apply the normalization on the passed image
        """
        image /= 255
        return image


class DenormalizeYolo(Processing):
    """
    Denormalize an image by scaling the pixel values from between 0 and 1 to between 0 and 255

    """

    def __init__(self):
        super().__init__()

    def apply(self, image: torch.Tensor):
        """
        Apply the denormalization on the passed image
        """
        image = image * 255
        return image
