import numpy as np

from elements.settings.general_settings import GeneralSettings


class BoxProcessor:
    """
    A BoxProcessor instance is responsible for taking in (postprocessed) predictions of a YOLO model and constructing a readable numpy array from it
    """

    def __init__(self, general_settings: GeneralSettings):
        self.general_settings = general_settings

    def extract_boxes(self, predictions: np.ndarray) -> list[np.ndarray]:
        """
        Constructs a numpy array from raw YOLO predictions [x1, y1, x2, y2, confidence, class_id]
        """
        boxes_numpy = []
        for box in predictions[0]:
            if box.boxes.conf.item() > self.general_settings.box_threshold:
                if self.general_settings.classes[int(box.boxes.cls.item())] in self.general_settings.tracked_classes:
                    new_box = np.asarray(box.boxes.xyxy.tolist()[0] + [box.boxes.conf.item()] + [box.boxes.cls.item()])
                    boxes_numpy.append(new_box)
        return boxes_numpy
