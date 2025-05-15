import gradio as gr

from elements.enums import Tasks, InputMode
from elements.locker import Locker
from elements.settings.params.param_settings import ParamSetting


class AdvancedViewSetting(ParamSetting):
    """
    The AdvancedView toggle in the GUI toggles more advanced parameters that can be changed.

    Task: TRACKING
    Note: The task itself is often a condition as well

    Visible Field                  | Condition
    -------------------------------|--------------------------------------------------------------
    Realistic Processing             | camera_mode == InputMode.FILE
    Box threshold
    Detection threshold            | advanced_view == True
    Minimum hits                   | advanced_view == True
    Maximum age                    | advanced_view == True

    Task: Other Tasks
    Field                          | Visible
    -------------------------------|--------------------------------------------------------------
    Bit                            | advanced_view == True
    Width input model              | advanced_view == True
    Height input model             | advanced_view == True
    Box threshold
    Gamma correction               | advanced_view == True
    Gamma value                    | advanced_view == True

    """
    def __init__(self, general_settings, tracking_settings, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.tracking_settings = tracking_settings

    def update(self, advanced_view: bool, **params):
        with self.locker.lock:
            self.logger.info(f"Changed advanced view {str(self.general_settings.advanced_view)} to {str(advanced_view)}")

            if self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold():
                bit_box = gr.Dropdown(choices=["6", "8", "10", "12", "14", "16"], label="Bit", interactive=True, value=str(self.general_settings.bpp), visible=False)
                width_input_box = gr.Text(label="Width input model", value=self.general_settings.input_width, interactive=True, visible=advanced_view)
                height_input_box = gr.Text(label="Height input model", value=self.general_settings.input_height, interactive=True, visible=advanced_view)

            realistic_processing_box = gr.Checkbox(label="Slow down processing", interactive=True, value=self.general_settings.realistic_processing, visible=True if self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold() and self.general_settings.camera_mode == InputMode.FILE else False)
            box_threshold_box = gr.Text(label="Box threshold", interactive=True, value=str(self.general_settings.box_threshold), visible=True)
            gamma_correction_bool_box = gr.Checkbox(label="Gamma correction", interactive=True, value=self.general_settings.gamma_correction_bool, visible=advanced_view and not self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold())
            gamma_correction_value_box = gr.Text(label="Gamma value", interactive=True, value=str(self.general_settings.gamma_correction_value), visible=advanced_view and not self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold())

            tracker_option_1 = gr.Text(label="Detection threshold", value=str(self.tracking_settings.param_options.get(self.tracking_settings.current_options[0], "-")), interactive=True, visible=False)  # Redundant as there is already a box threshold setting
            tracker_option_2 = gr.Text(
                label="Minimum hits",
                value=str(self.tracking_settings.param_options.get(self.tracking_settings.current_options[1], "-")),
                interactive=True,
                visible=advanced_view and self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold() is not None and not self.tracking_settings.current_options[1] == ""
            )
            tracker_option_3 = gr.Text(
                label="Maximum age",
                value=str(self.tracking_settings.param_options.get(self.tracking_settings.current_options[2], "-")),
                interactive=True,
                visible=advanced_view and self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold() is not None and not self.tracking_settings.current_options[2] == ""
            )
            tracker_option_4 = gr.Text(
                label="_", value=str(self.tracking_settings.param_options.get(self.tracking_settings.current_options[3], "-")), interactive=True, visible=advanced_view and self.general_settings.task_type.casefold() == Tasks.TRACKING.name.casefold() is not None and not self.tracking_settings.current_options[3] == ""
            )

        return bit_box, width_input_box, height_input_box, box_threshold_box, gamma_correction_bool_box, gamma_correction_value_box, tracker_option_1, tracker_option_2, tracker_option_3, tracker_option_4, realistic_processing_box
