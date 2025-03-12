import os
import sys
from argparse import ArgumentParser

import gradio as gr

import src.js
from elements.enums import Tasks, InputMode
from elements.settings.model_settings import ModelSettings
from elements.settings.general_settings import GeneralSettings
from elements.settings.settings_orchestrator import SettingsOrchestrator
from elements.settings.tracking_settings import TrackingSettings
from gradio_server.css_injection import css_injection
from gradio_server.model_manager import ModelManager

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

parser = ArgumentParser(description='')
parser.add_argument('--type', type=str, default='tracking')
parser.add_argument('--template', type=str, default="bikehelmets")
parser.add_argument('--screen-width', type=int, default=1920)
parser.add_argument('--screen-height', type=int, default=1080)

args = parser.parse_args()

general_settings = GeneralSettings()
model_settings = ModelSettings()
tracking_settings = TrackingSettings()

model_manager = ModelManager(args)
model_manager.initialize_settings(general_settings=general_settings, model_settings=model_settings, tracking_settings=tracking_settings)

config = model_manager.get_parsed_config()

setting_orchestrator = SettingsOrchestrator(model_manager=model_manager)
setting_orchestrator.initialize_values(config=config.current_config)

setting_orchestrator.camera_mode_setting.update(InputMode.FILE)  # On default, the GUI is suitable for video input mode
setting_orchestrator.screen_dimension_setting.update(width=args.screen_width, height=args.screen_height)

model_manager.start_websocket_server()

demo = gr.Blocks(theme=gr.themes.Default(text_size=gr.themes.sizes.text_lg),
                 css=css_injection)

if Tasks.TRACKING.name.casefold() in args.type.casefold():
    with demo:
        with gr.Row():
            with gr.Column():
                with gr.Column():
                    camera_button = gr.Button(value="Set to camera mode", interactive=True)
                    advanced_view = gr.Checkbox(label="Advanced mode", interactive=True, value=model_manager.general_settings.advanced_view)
                    output_folder = gr.Text(label="Output folder for the tracking results", value=model_manager.general_settings.output_folder, interactive=False)
                    model_architectures = gr.Dropdown(choices=[config.architecture for config in config.task_type_models[args.type]], label="Model architectures", value=model_manager.model_settings.architecture, interactive=True)
                    weights = gr.Radio(label="Model weights", interactive=True, choices=[a_config.weights for a_config in config.all_configs if a_config.architecture == config.current_config.architecture], value=config.current_config.weights)
                    bit_box = gr.Dropdown(choices=["6", "8", "10", "12", "14", "16"], label="Bit", interactive=True, value=str(model_manager.general_settings.bpp), visible=False)
                    device_box = gr.Dropdown(choices=["cpu", "cuda:0"], label="Device", interactive=True, value=str(model_manager.model_settings.device))

                    width_input_box = gr.Text(label="Width input model", interactive=True, visible=False)
                    height_input_box = gr.Text(label="Height input model", interactive=True, visible=False)
                    width_input_box.change(setting_orchestrator.input_width_setting.update, inputs=width_input_box)
                    height_input_box.change(setting_orchestrator.input_height_setting.update, inputs=height_input_box)

                    box_threshold_box = gr.Text(label="Box threshold", interactive=True, value=str(general_settings.box_threshold), visible=True)
                    box_threshold_box.change(setting_orchestrator.box_threshold_setting.update, inputs=box_threshold_box)

                    realistic_processing_box = gr.Checkbox(label="Realistic Processing", interactive=True, value=general_settings.realistic_processing, visible=True)
                    realistic_processing_box.change(setting_orchestrator.realistic_processing_setting.update, inputs=realistic_processing_box)

                    gamma_correction_bool_box = gr.Checkbox(label="Gamma correction", interactive=True, value=general_settings.gamma_correction_bool, visible=False)
                    gamma_value_box = gr.Text(label="Gamma value", interactive=True, value=str(general_settings.gamma_value), visible=False)

                with gr.Column():
                    trackers = gr.Dropdown(label="Trackers", interactive=True, choices=config.trackers)
                    tracker_option_1 = gr.Text(label="high Tracking threshold", value=str(tracking_settings.param_options["HIGH_TRACKING_THRESHOLD"]), interactive=True, visible=False)
                    tracker_option_2 = gr.Text(label="Low Tracking threshold", value=str(tracking_settings.param_options["LOW_TRACKING_THRESHOLD"]), interactive=True, visible=False)
                    tracker_option_3 = gr.Text(label="Matching threshold", value=str(tracking_settings.param_options["MATCHING_THRESHOLD"]), interactive=True, visible=False)
                    tracker_option_4 = gr.Text(label="Tracking buffer", value=str(tracking_settings.param_options["TRACKING_BUFFER"]), interactive=True, visible=False)
                    trackers.change(setting_orchestrator.tracker_setting.update, inputs=trackers, outputs=[tracker_option_1, tracker_option_2, tracker_option_3, tracker_option_4])

                    tracker_option_1.change(setting_orchestrator.tracker_option_1_setting.update, inputs=tracker_option_1)
                    tracker_option_2.change(setting_orchestrator.tracker_option_2_setting.update, inputs=tracker_option_2)
                    tracker_option_3.change(setting_orchestrator.tracker_option_3_setting.update, inputs=tracker_option_3)
                    tracker_option_4.change(setting_orchestrator.tracker_option_4_setting.update, inputs=tracker_option_4)

                with gr.Column():
                    check_boxes = gr.CheckboxGroup(label="Which objects should be tracked", choices=config.current_config.classes, value=config.current_config.classes, interactive=True)

            with gr.Column():
                input_image_box = gr.File(label="Input video", elem_id="video_in")

                analysis_button = gr.Button(interactive=True, value="Start camera analysis", visible=False)  # Can start and stop camera feed analysis, but also cancel video analysis
                reset_tracker_stats_button = gr.Button(interactive=True, value="Reset tracker stats", visible=False)
                image_out_box = gr.Video(interactive=False, elem_id="video_out", height="auto", width=1500)

                input_image_box.upload(fn=model_manager.predict_gui, inputs=[input_image_box], outputs=[analysis_button, reset_tracker_stats_button])

        analysis_button.click(model_manager.toggle_analysis, outputs=[analysis_button, reset_tracker_stats_button])
        camera_button.click(model_manager.switch_camera_mode, outputs=[camera_button, input_image_box, analysis_button, reset_tracker_stats_button])
        reset_tracker_stats_button.click(model_manager.reset_tracker)

        advanced_view.change(setting_orchestrator.advanced_view_setting.update, inputs=advanced_view,
                             outputs=[bit_box, width_input_box, height_input_box, box_threshold_box, gamma_correction_bool_box, gamma_value_box, tracker_option_1, tracker_option_2, tracker_option_3, tracker_option_4, realistic_processing_box])

        device_box.change(setting_orchestrator.device_setting.update, inputs=device_box)
        bit_box.change(setting_orchestrator.bpp_setting.update, inputs=bit_box)

        gamma_correction_bool_box.change(setting_orchestrator.gamma_correction_bool_setting.update, inputs=gamma_correction_bool_box)
        gamma_value_box.change(setting_orchestrator.gamma_correction_value_setting.update, inputs=gamma_value_box)
        check_boxes.change(setting_orchestrator.classes_setting.update, inputs=check_boxes)

        output_folder.change(setting_orchestrator.output_folder_setting.update, inputs=output_folder)

        model_architectures.change(fn=setting_orchestrator.architecture_setting.update,
                                   inputs=model_architectures,
                                   outputs=[weights, width_input_box, height_input_box, check_boxes])

        weights.change(fn=setting_orchestrator.weights_setting.update,
                       inputs=weights,
                       outputs=check_boxes)

        demo.load(fn=None, js=src.js.script_new)

demo.launch()
