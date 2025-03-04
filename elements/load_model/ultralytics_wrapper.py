# Parts of the code are derived from the YoloV5 repository of Ultralytics,  https://github.com/ultralytics/yolov5.
# Note: version 4.0, downloaded January 2021.
# This Yolo repository is released under the GNU General Public License v3.0 licence.

# todo for new version of this repro do:
# - utils/general.py: comment out 2x set_printoptions
# - run yolov5_convert_model.py and copy *.pth to yolo_conf_dir


import os
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.utils.data
from ultralytics.cfg import get_cfg
from ultralytics.utils.checks import check_imgsz
from ultralytics.utils.loss import v8DetectionLoss
from ultralytics.utils.ops import non_max_suppression

try:
    import ultralytics
    from ultralytics.nn.tasks import DetectionModel, RTDETRDetectionModel
    from ultralytics.models.utils.loss import RTDETRDetectionLoss
    from ultralytics import YOLO

    # from yolov5.utils.general import non_max_suppression, check_img_size, intersect_dicts
    # from yolov5.utils.loss import ComputeLoss

    # reset printoptions to default and logger defined in the yolov5 library (general file)
    ultralytics.utils.VERBOSE = False
    ultralytics.utils.set_logging(verbose=False)
    torch.set_printoptions(profile="default")  # as suggested by https://pytorch.org/docs/stable/_modules/torch/_tensor_str.html#set_printoptions
    np.set_printoptions(edgeitems=3, infstr='inf', linewidth=75, nanstr='nan', precision=8, suppress=False, threshold=1000, formatter=None)  # as specified by https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
except:
    pass


class Yolo(nn.Module):
    """Yolo object detector."""

    def __init__(self, architecture: str, model_name: str, num_classes: int, weights_file: str, num_chans=3, device='cuda:0', pretrained=False, yolo_conf_dir: str = os.path.join('models', 'architectures')):
        """
        The Yolo constructor.

        :param model_name: the name of the Yolo model. ('yolov[x]n', 'yolov[x]s', 'yolov[x]m', 'yolov[x]l' or 'yolov[x]x', where [x] is the version of Yolo to be created (either 5, 8, 9, 10, 11)
        :param num_classes: the number of classes.
        :param num_chans: the number of channels in the images.
        :param device: the device to run the model on.
        :param pretrained: True if pretrained on COCO dataset should be loaded.
        """
        super().__init__()
        self.yolo_conf_dir = yolo_conf_dir
        hyp = get_cfg(cfg=os.path.join(yolo_conf_dir, 'cfg', 'default.yaml'))
        self.num_classes = num_classes
        self.class_names = [str(c) for c in range(num_classes)]
        cfg_name = model_name + '.yaml'
        self.model = YOLO(model_name)
        if pretrained:
            filename = os.path.join(yolo_conf_dir, architecture, weights_file)
            if not os.path.isfile(filename): raise RuntimeError(f'No pretrained file with name: {filename}')
            self.model.load(weights=torch.load(filename))
            hyp.pretrained = True
        hyp.cls *= self.num_classes / 80.  # scale coco-tuned hyp['cls'] to current dataset
        self.model.nc = self.num_classes
        # self.model.names = self.class_names
        self.model.args = hyp
        self.model.gr = 1.0
        # self.model.class_weights = np.ones(self.num_classes, dtype=np.float32) / self.num_classes
        # self.loss_fn = v8DetectionLoss(self.model)

    def optimal_image_size(self, image_size):
        """Calculate the optimal image size for network."""
        max_stride = int(max(self.model.stride))
        return check_imgsz(image_size, max_stride)

    def forward(self, inputs: torch.Tensor):
        """
        The inference function.

        :param inputs: Tensor of shape NxCxHxW.
        :return: (raw_detections and) feature map.

        If in training mode, the predictions (feature map, tensor for each scale) are returned as tuple[0]:
        list[B x 3 x cell_v X cell_h x (xyhw_object_conf + numclss*conf_cls), 3 = nr predictions per cell.
        Predictions can be used as input to the loss function.
        If in eval mode, both raw_detections and predictions are returned as tuple[0] and tuple[1].
        Raw_detections are flattened predictions: Tensor [B x (3 x nr_cells_over_all_3_levels) x (xyhw_object_conf + numclss*conf_cls).
        Raw_detections can be used as input to the detections function.
        """
        preds = self.model(inputs)
        return preds

    def loss(self, preds: tuple[Any, ...], targets: dict) -> tuple[torch.Tensor, torch.Tensor]:
        """
        The loss function for training.

        :param preds: the predictions from function forward.
        :param targets: the target bounding boxes in the following format:
            {
                "batch_idx": torch.Tensor([N]),
                "cls": torch.Tensor([N]),
                "bboxes": torch.Tensor([N, 4])  # x_ctr, y_ctr, width, height
                }
                Where N is the number of bounding boxes
        :return: the overall loss (sum of all losses * batch_size), [box loss, class loss, DFL loss].
        """
        overall_loss, loss = self.loss_fn(preds[len(preds) - 1], targets)
        return overall_loss, loss

    def detections(self, preds: tuple[Any, ...]) -> list[torch.Tensor]:
        """
        Calculate detections from raw detections.

        :param preds: the predictions from function forward.
        :return: a list with for each image a tensor of bounding boxes [y1, x1, y2, x2, class, score].
        """
        detects = non_max_suppression(preds[0])
        # yolo detections format: list with for each image torch tensor with detections: [x1, y1, x2, y2, conf, cls], sorted on conf
        res = []
        for preds in detects:
            if preds is not None:
                dets = torch.empty_like(preds, device=torch.device('cpu'))
                dets[:, 0] = preds[:, 1]
                dets[:, 1] = preds[:, 0]
                dets[:, 2] = preds[:, 3]
                dets[:, 3] = preds[:, 2]
                dets[:, 4] = preds[:, 5]
                dets[:, 5] = preds[:, 4]
                res.append(dets)
            else:
                res.append(torch.empty([0, 6]))  # add dummy
        return res


class DETR(nn.Module):
    """DETR object detector."""

    def __init__(self, model_name: str, num_classes: int, num_chans=3, device='cuda:0', pretrained=False,
                 yolo_conf_dir: str = '/media/public_data/datasets/models/ultralytics/'):
        """
        The DETR constructor.

        :param model_name: the name of the DETR model. ('rtdetr-l', 'rtdetr-x')
        :param num_classes: the number of classes.
        :param num_chans: the number of channels in the images.
        :param device: the device to run the model on.
        :param pretrained: True if pretrained on COCO dataset should be loaded.
        """
        super().__init__()
        self.yolo_conf_dir = yolo_conf_dir
        hyp = get_cfg(cfg=os.path.join(yolo_conf_dir, 'cfg', model_name + ".yaml"))
        self.num_classes = num_classes
        self.class_names = [str(c) for c in range(num_classes)]
        cfg_name = model_name + '.yaml'
        self.model = RTDETRDetectionModel(cfg_name, ch=num_chans, nc=self.num_classes).to(device)
        if pretrained:
            filename = os.path.join(yolo_conf_dir, f'{model_name}.pt')
            if not os.path.isfile(filename): raise RuntimeError(f'No pretrained file with name: {filename}')
            self.model.load(weights=torch.load(filename))
            hyp.pretrained = True
        # self.model.training = False
        # self.model.model.training = False
        # hyp.cls *= self.num_classes / 80.  # scale coco-tuned hyp['cls'] to current dataset
        self.model.nc = self.num_classes
        self.model.names = self.class_names
        self.model.args = hyp
        self.model.gr = 1.0
        self.model.class_weights = np.ones(self.num_classes, dtype=np.float32) / self.num_classes

        self.loss_fn = RTDETRDetectionLoss(nc=self.num_classes, use_vfl=True)
        self.loss_fn.device = device

    def optimal_image_size(self, image_size):
        """Calculate the optimal image size for network."""
        max_stride = int(max(self.model.stride))
        return check_imgsz(image_size, max_stride)

    def forward(self, inputs: torch.Tensor) -> tuple[Any, ...]:
        """
        The inference function.

        :param inputs: Tensor of shape NxCxHxW.
        :return: (raw_detections and) feature map.

        If in training mode, the predictions (feature map, tensor for each scale) are returned as tuple[0]:
        list[B x 3 x cell_v X cell_h x (xyhw_object_conf + numclss*conf_cls), 3 = nr predictions per cell.
        Predictions can be used as input to the loss function.
        If in eval mode, both raw_detections and predictions are returned as tuple[0] and tuple[1].
        Raw_detections are flattened predictions: Tensor [B x (3 x nr_cells_over_all_3_levels) x (xyhw_object_conf + numclss*conf_cls).
        Raw_detections can be used as input to the detections function.
        """
        preds = self.model(inputs)
        if self.model.training:
            return preds,  # feature map
        else:  # eval mode
            return preds[0], preds[1]  # raw detections, feature pyramid map

    def loss(self, preds: tuple[Any, ...], targets: dict) -> torch.Tensor:
        """
        The loss function for training.

        :param preds: the predictions from function forward.
        :param targets: the target bounding boxes in the following format:
            {
                "batch_idx": torch.Tensor([N]),
                "cls": torch.Tensor([N]),
                "bboxes": torch.Tensor([N, 4])  # x_ctr, y_ctr, width, height
                }
                Where N is the number of bounding boxes
        :return: the loss.
        """
        return self.loss_fn(preds[len(preds) - 1], targets)[0]

    def detections(self, preds: tuple[Any, ...]) -> list[torch.Tensor]:
        """
        Calculate detections from raw detections.

        :param preds: the predictions from function forward.
        :return: a list with for each image a tensor of bounding boxes [y1, x1, y2, x2, class, score].
        """
        detects = non_max_suppression(preds[0])
        # yolo detections format: list with for each image torch tensor with detections: [x1, y1, x2, y2, conf, cls], sorted on conf
        res = []
        for preds in detects:
            if preds is not None:
                dets = torch.empty_like(preds, device=torch.device('cpu'))
                dets[:, 0] = preds[:, 1]
                dets[:, 1] = preds[:, 0]
                dets[:, 2] = preds[:, 3]
                dets[:, 3] = preds[:, 2]
                dets[:, 4] = preds[:, 5]
                dets[:, 5] = preds[:, 4]
                res.append(dets)
            else:
                res.append(torch.empty([0, 6]))  # add dummy
        return res
