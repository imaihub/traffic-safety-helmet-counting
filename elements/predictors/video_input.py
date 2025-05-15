import time
import traceback

import gradio as gr
import torch

from elements.enums import ApplicationMode
from elements.locker import Locker
from elements.predictors.base_predictor import PredictorBase
from elements.predictors.parameters import PredictorParameters
from elements.predictors.utils.video_reader import VideoReader
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.tracking_settings import TrackingSettings
from elements.benchmark_timer import BenchmarkTimer
from gradio_server.websocket_manager.websocket_manager import WebSocketServer


class PredictorTrackerInput(PredictorBase):
    """
    A PredictorTrackerInputLive  is a type of Predictor that is responsible for the tracking of objects in a given video.
    """
    def __init__(self, general_settings: GeneralSettings, model_settings: ModelSettings, tracking_settings: TrackingSettings, predictor_parameters: PredictorParameters, websocket_server: WebSocketServer, locker: Locker):
        super().__init__(general_settings=general_settings, model_settings=model_settings, tracking_settings=tracking_settings, predictor_parameters=predictor_parameters, websocket_server=websocket_server, locker=locker)

    @torch.no_grad()
    def predict(self):
        """
        Processes a single video from the input_path passed.
        """
        try:
            if self.general_settings.application_mode == ApplicationMode.GUI:
                self.wait_for_websocket()

            with VideoReader(self.predictor_parameters.input_path) as video_reader:
                self.result_saver.initiate_result_video(width=self.general_settings.screen_width, height=self.general_settings.screen_height, fps=video_reader.fps)

                with self.result_saver:
                    for current_frame, image in video_reader.frames(skip_frames=self.predictor_parameters.skip_frames):
                        try:
                            with BenchmarkTimer("Process frame", wait_time=(1 / video_reader.fps) * 1000 if self.general_settings.realistic_processing else 0, print_time=False) as processing_timer:
                                if self.aborting:
                                    break

                                if current_frame % 50 == 0:
                                    gr.Info(f"{(current_frame / video_reader.total_frames) * 100}% Done", duration=2)

                                while self.model_settings.model is None:
                                    self.logger.info("Waiting for model to be loaded...")
                                    time.sleep(0.1)

                                self.locker.lock.acquire()

                                if self.tracking_settings.reset:
                                    self.update_settings()

                                show_image, save_image = self.process_frame(image=image, display=self.predictor_parameters.display)

                                self.locker.lock.release()

                                if self.general_settings.save_results:
                                    self.result_saver.append_image_to_video(image=show_image)

                                if self.general_settings.save_new_objects and save_image:
                                    self.result_saver.save_image(image=show_image)

                                self.set_response(image=show_image)
                        except Exception as e:
                            self.logger.error(traceback.format_exc())
                            self.logger.error(e)
                            if self.locker.lock.locked():
                                self.locker.lock.release()

            if self.general_settings.application_mode == ApplicationMode.GUI:
                self.websocket.finish_connection()

        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
