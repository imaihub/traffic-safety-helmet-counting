import traceback

import gradio as gr
import numpy as np
import torch

from elements.data.predictor_parameters import PredictorParameters
from elements.enums import ApplicationMode
from elements.predictors.base_predictor import PredictorBase
from elements.predictors.utils.video_reader import VideoReader
from elements.timer import Timer
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.model_settings import ModelSettings
from gradio_server.websocket_manager.websocket_manager_upload import WebSocketServerUpload


class PredictorTrackerInput(PredictorBase):
    """
    A PredictorTrackerInputLive  is a type of Predictor that is responsible for the tracking of objects in a given video.
    It returns the path of a fully analyzed video for Gradio to show it. This means users don't get to see "realtime" analysis
    """

    def __init__(self, model: torch.nn.Module, general_settings: GeneralSettings, model_settings: ModelSettings, predictor_parameters: PredictorParameters, websocket_server: WebSocketServerUpload):
        super().__init__(model, general_settings, model_settings, predictor_parameters, websocket_server)
        self.last_times = [0, 0]


    @torch.no_grad()
    def predict(self):
        """
        Processes a single video from the input_path passed. Returns the path with a copy of the resulting video for Gradio
        """
        try:
            if self.general_settings.application_mode == ApplicationMode.GUI:
                self.wait_for_websocket()

            with VideoReader(self.predictor_parameters.input_path) as video_reader:
                self.result_saver.initiate_result_video(width=1920, height=1080, fps=video_reader.fps)

                with self.result_saver:
                    for current_frame, image in video_reader.frames(skip_frames=self.predictor_parameters.skip_frames):
                        if self.aborting:
                            break

                        if current_frame % 50 == 0:
                            gr.Info(f"{(current_frame / video_reader.total_frames) * 100}% Done", duration=2)

                        processing_timer = Timer("Process frame")
                        processing_timer.start()

                        if self.general_settings.dynamic_processing:
                            frames_to_skip = int(np.mean(self.last_times) * video_reader.fps) - 1
                            frames_to_skip = max(0, frames_to_skip)  # Ensure frames_to_skip is not negative
                            if not current_frame == frames_to_skip:
                                current_frame += 1
                                continue

                        show_image, save_image = self.process_frame(image=image, display=self.predictor_parameters.display)

                        self.result_saver.append_image_to_video(image=show_image)
                        if save_image:
                            self.result_saver.save_image(image=show_image)

                        self.set_response(image=show_image)

                        processing_timer.stop()

                        self.last_times.append(processing_timer.get_timings()["real_time"])
                        if len(self.last_times) > 5:
                            self.last_times = self.last_times[1:]

            self.websocket.finish_connection()
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
