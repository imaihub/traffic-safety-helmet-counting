import os
import sys
from argparse import ArgumentParser

from elements.display import Display
from elements.enums import InputMode, ApplicationMode
from gradio_server.model_manager import ModelManager
from gradio_server.settings.general_settings import GeneralSettings
from gradio_server.settings.model_settings import ModelSettings
from gradio_server.settings.settings_orchestrator import SettingsOrchestrator
from gradio_server.settings.tracking_settings import TrackingSettings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

parser = ArgumentParser(description='')
parser.add_argument('--type', type=str, default='tracking')
parser.add_argument('--camera-mode', action="store_true")
parser.add_argument('--template', type=str, default="bikehelmets")
parser.add_argument('--input', type=str, default="output.mp4")

args = parser.parse_args()

general_settings = GeneralSettings()
model_settings = ModelSettings()
tracking_settings = TrackingSettings()

model_manager = ModelManager(args)
model_manager.initialize_settings(general_settings=general_settings, model_settings=model_settings, tracking_settings=tracking_settings)

config = model_manager.get_parsed_config()

setting_orchestrator = SettingsOrchestrator(model_manager=model_manager)
setting_orchestrator.initialize_values(config=config.current_config)

general_settings.application_mode = ApplicationMode.CLI

display = Display()

if args.camera_mode:
    setting_orchestrator.camera_mode_setting.update(InputMode.CAMERA)
    model_manager.predict(input_path=None, display=display)
else:
    setting_orchestrator.camera_mode_setting.update(InputMode.FILE)
    full_input_path = os.path.join("dataset", args.input)
    model_manager.predict(input_path=full_input_path, display=display)


