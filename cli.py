import os
import sys
from argparse import ArgumentParser

from elements.display import Display
from elements.enums import InputMode, ApplicationMode
from elements.locker import Locker
from elements.predictors.tracking_predictor import PredictTracking
from elements.settings.general_settings import GeneralSettings
from elements.settings.model_settings import ModelSettings
from elements.settings.settings_orchestrator import SettingsOrchestrator
from elements.settings.tracking_settings import TrackingSettings
from gradio_server.model_manager import ModelManager

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

parser = ArgumentParser(description='')
parser.add_argument('--type', type=str, default='tracking')
parser.add_argument('--realistic', action="store_true")
parser.add_argument('--camera-mode', action="store_true")
parser.add_argument('--gpu', action="store_true")
parser.add_argument('--template', type=str, default="bikehelmets")
parser.add_argument('--input', type=str, default="output.mp4")
parser.add_argument('--screen-width', type=int, default=1920)
parser.add_argument('--screen-height', type=int, default=1080)
parser.add_argument('--camera-width', type=int, default=1920)
parser.add_argument('--camera-height', type=int, default=1080)
parser.add_argument('--camera-index', type=int, default=0)
parser.add_argument('--save-all-frames', action="store_true")
parser.add_argument('--reset-stats-min', type=float, default=0.0)

args = parser.parse_args()

general_settings = GeneralSettings()
model_settings = ModelSettings()
tracking_settings = TrackingSettings()

model_manager = ModelManager(args)
model_manager.initialize_settings(general_settings=general_settings, model_settings=model_settings,
                                  tracking_settings=tracking_settings)

config = model_manager.get_parsed_config()
full_input_path = os.path.join("dataset", args.input)

setting_orchestrator = SettingsOrchestrator(model_manager=model_manager)

setting_orchestrator.device_setting.update(device="cuda:0" if args.gpu else "cpu")
setting_orchestrator.realistic_processing_setting.update(realistic_processing=args.realistic)
setting_orchestrator.screen_dimension_setting.update(width=args.screen_width, height=args.screen_height)
setting_orchestrator.camera_dimension_setting.update(width=args.camera_width, height=args.camera_height)
setting_orchestrator.camera_index_setting.update(index=args.camera_index)
setting_orchestrator.save_all_frames_setting.update(save_all_frames=args.save_all_frames)
setting_orchestrator.reset_stats_min.update(minutes=args.reset_stats_min)
setting_orchestrator.initialize_values(config=config.current_config)

general_settings.application_mode = ApplicationMode.CLI
locker = Locker()
display = Display()

if args.camera_mode:
    setting_orchestrator.camera_mode_setting.update(InputMode.CAMERA)
    predictor, predictor_parameters = PredictTracking(general_settings=general_settings,
                                                      model_settings=model_settings,
                                                      tracking_settings=tracking_settings,
                                                      display=display).get_predictor()

    predictor.predict(locker=locker)
else:
    setting_orchestrator.camera_mode_setting.update(InputMode.FILE)
    predictor, predictor_parameters = PredictTracking(general_settings=general_settings,
                                                      model_settings=model_settings,
                                                      tracking_settings=tracking_settings,
                                                      display=display,
                                                      input_path=full_input_path).get_predictor()

    predictor.predict(locker=locker)
