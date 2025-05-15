from typing import Tuple, Any

import torch
from torch import Tensor


def decode_yolo_boxes_pt(model: torch.nn.Module, preds: Tuple[Any, ...], image_batch: torch.Tensor, margin: int = 0) -> list[Tensor]:
    """
    Decode the output of YoloV8 to create boxes.

    :param model: The model
    :param preds: The predictions output of :meth:`elements.predict.detection.predict_yolov5_pt`
    :param image_batch: The original image_batch that provided the raw_boxes
    :param margin: Boxes outside this margin will be rejected

    :return: Decoded boxes containing [[y1, x1, y2, y2, class_id, class_prob]]

    """
    bboxes_batch = model.detections(preds)
    if margin > 0:  # Check if centroid is outside border margin
        h, w = image_batch.shape[-2:]
        res = []
        for bboxes in bboxes_batch:
            if len(bboxes):
                bboxes = bboxes[(bboxes[:, 0] + bboxes[:, 2]) / 2 > margin, :]
                bboxes = bboxes[(bboxes[:, 1] + bboxes[:, 3]) / 2 > margin, :]
                bboxes = bboxes[(bboxes[:, 0] + bboxes[:, 2]) / 2 < w - margin, :]
                bboxes = bboxes[(bboxes[:, 1] + bboxes[:, 3]) / 2 < h - margin, :]
            res.append(bboxes)
        bboxes_batch = res
    return bboxes_batch
