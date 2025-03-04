import numpy as np


class BoxProcessor:
    """
    A BoxProcessor instance is responsible for taking in (postprocessed) predictions of a YOLO model and constructing a readable numpy array from it
    """
    def __init__(self, tracker_processor, tracked_classes: list, classes: list, box_threshold: float):
        self.tracker_processor = tracker_processor
        self.tracked_classes = tracked_classes
        self.classes = classes
        self.box_threshold = box_threshold

    def extract_boxes(self, predictions):
        """
        Constructs a numpy array from raw YOLO predictions [x1, y1, x2, y2, confidence, class_id]
        """
        boxes_numpy = []
        for box in predictions[0]:
            if box.boxes.conf.item() > self.box_threshold:
                if self.classes[int(box.boxes.cls.item())] in self.tracked_classes:
                    new_box = np.asarray(box.boxes.xyxy.tolist()[0] + [box.boxes.conf.item()] + [box.boxes.cls.item()])
                    boxes_numpy.append(new_box)
        return boxes_numpy
