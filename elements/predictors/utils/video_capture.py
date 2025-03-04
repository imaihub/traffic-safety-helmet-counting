import cv2


class VideoCapture:
    """
    A VideoCapture instance is responsible for reading images from the webcam and returning it frame for frame in a generator method.
    """

    def __init__(self):
        self.vidcap = cv2.VideoCapture(0)

    def __enter__(self):
        return self

    def frames(self):
        success, image = self.vidcap.read()
        while success:
            yield image
            success, image = self.vidcap.read()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def release(self):
        self.vidcap.release()
