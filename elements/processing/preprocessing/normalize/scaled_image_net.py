import torch

from elements.processing.base import Processing


class NormalizeScaledImageNet(Processing):
    """
    Normalize an image using scaled (using the max pixel value derived the bit value of the camera used) from ImageNet mean and std values
    """

    def __init__(self, bit: int = 8):
        super().__init__()
        self.type = type
        self.bit = bit
        self.bit_range = 2 ** self.bit - 1
        self.mean = torch.tensor([0.485 * self.bit_range, 0.456 * self.bit_range, 0.406 * self.bit_range], dtype=torch.float32).view((3, 1, 1))
        self.std = torch.tensor([0.229 * self.bit_range, 0.224 * self.bit_range, 0.225 * self.bit_range], dtype=torch.float32).view((3, 1, 1))

    def apply(self, img: torch.Tensor):
        """
        Apply the normalization on the passed image
        """
        img -= self.mean.to(img.device)
        img /= self.std.to(img.device)

        return img


class DenormalizeScaledImageNet(Processing):
    """
    Denormalize an image using scaled (using the max pixel value derived the bit value of the camera used) from ImageNet mean and std values
    """

    def __init__(self, bit: int = 8):
        super().__init__()
        self.type = type
        self.bit = bit
        self.bit_range = 2 ** self.bit - 1
        self.mean = torch.tensor([0.485 * self.bit_range, 0.456 * self.bit_range, 0.406 * self.bit_range], dtype=torch.float32).view(3, 1, 1)
        self.std = torch.tensor([0.229 * self.bit_range, 0.224 * self.bit_range, 0.225 * self.bit_range], dtype=torch.float32).view(3, 1, 1)

    def apply(self, img: torch.Tensor):
        """
        Apply the denormalization on the passed image
        """
        img = (img * self.std.to(img.device)) + self.mean.to(img.device)

        # Ensure the image values are within the original range
        img.clamp_(0, self.bit_range).to(torch.uint8)

        return img
