import time
import traceback

import cv2
import torch

from elements.locker import Locker
from elements.predictors.base_predictor import PredictorBase
from elements.predictors.parameters import PredictorParameters
from elements.predictors.utils.video_capture import VideoCapture
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.tracking_settings import TrackingSettings
from gradio_server.websocket_manager.websocket_manager import WebSocketServer


class PredictorTrackerCamera(PredictorBase):
    """
    A PredictorTrackerCamera is a type of Predictor that is responsible for the tracking of objects in a camera feed.
    """

    def __init__(self,
                 general_settings: GeneralSettings,
                 model_settings: ModelSettings,
                 tracking_settings: TrackingSettings,
                 predictor_parameters: PredictorParameters,
                 websocket_server: WebSocketServer,
                 locker: Locker):
        super().__init__(general_settings=general_settings,
                         model_settings=model_settings,
                         tracking_settings=tracking_settings,
                         predictor_parameters=predictor_parameters,
                         websocket_server=websocket_server,
                         locker=locker)
        self.result_saver.initiate_result_video(width=self.general_settings.screen_width,
                                                height=self.general_settings.screen_height,
                                                fps=5)  # The FPS is as guess as this information is not available until later

    @torch.no_grad()
    def predict(self):
        """
        Processes a single passed image.
        """
        try:
            with VideoCapture(camera_index=self.general_settings.camera_index, save_directory=self.general_settings.output_folder) as video_capture:
                if video_capture.vidcap is None:
                    self.logger.error("No video capture available, aborting processing")
                    self.abort()
                    cv2.destroyAllWindows()
                    return None

                with self.result_saver:
                    for image in video_capture.frames(general_settings=self.general_settings):
                        try:
                            if self.aborting:
                                break

                            while self.model_settings.model is None:
                                self.logger.info("Waiting for model to be loaded...")
                                time.sleep(0.1)

                            self.locker.lock.acquire()

                            if self.tracking_settings.reset:
                                self.update_settings()

                            show_image, save_image = self.process_frame(image=image, display=self.predictor_parameters.display)
                            self.locker.lock.release()

                            self.result_saver.append_image_to_video(image=show_image)
                            if save_image:
                                self.result_saver.save_image(image=show_image)

                            self.set_response(image=show_image)

                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        except Exception as e:
                            traceback.print_exc()
                            self.logger.error(e)
                            if self.locker.lock.locked():
                                self.locker.lock.release()

            return show_image

        except Exception as e:
            self.logger.error(e)
            return None
