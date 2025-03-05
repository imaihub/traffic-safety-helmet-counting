import cv2
import torch

from elements.settings.model_settings import ModelSettings
from elements.predictors.base_predictor import PredictorBase
from elements.predictors.parameters import PredictorParameters
from elements.predictors.utils.video_capture import VideoCapture
from elements.settings.general_settings import GeneralSettings


class PredictorTrackerCamera(PredictorBase):
    """
    A PredictorTrackerCamera is a type of Predictor that is responsible for the tracking of objects in a camera feed.
    """

    def __init__(self, model: torch.nn.Module,
                 general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 predictor_parameters: PredictorParameters,
                 websocket_server):
        super().__init__(model, general_settings, model_settings, predictor_parameters, websocket_server)
        self.result_saver.initiate_result_video(width=1920, height=1080, fps=30)  # The FPS is as guess as this information is not available until later

    @torch.no_grad()
    def predict(self):
        """
        Processes a single passed image.
        """
        try:
            with self.result_saver:
                with VideoCapture() as video_capture:
                    for image in video_capture.frames():
                        if self.aborting:
                            break

                        show_image, save_image = self.process_frame(image=image, display=self.predictor_parameters.display)

                        self.result_saver.append_image_to_video(image=show_image)
                        if save_image:
                            self.result_saver.save_image(image=show_image)

                        self.set_response(image=show_image)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

            return show_image

        except Exception as e:
            self.logger.error(e)
