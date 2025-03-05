from elements.predictors.parameters import PredictorParameters
from elements.locker import Locker
from elements.settings.general_settings import GeneralSettings
from elements.settings.params.param_settings import ParamSetting
from elements.settings.tracking_settings import TrackingSettings
import gradio as gr


class TrackerSetting(ParamSetting):
    """
    Select the tracker to use to track objects throughout the video. Currently only DeepOCSort is implemented
    """

    def __init__(self, general_settings: GeneralSettings, tracking_settings: TrackingSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.tracking_settings = tracking_settings
        self.predictor_parameters = predictor_parameters

    def update(self, tracker: str):
        with self.locker.lock:
            self.logger.info(f"Changed tracker from {str(self.tracking_settings.tracker)} to {str(tracker)}")
            self.tracking_settings.tracker = tracker
            self.predictor_parameters = None

            match tracker.casefold():
                case "deepocsort":
                    self.tracking_settings.param_options["DETECTION_THRESHOLD"] = "0.4"
                    self.tracking_settings.param_options["MINIMUM_HITS"] = "5"
                    self.tracking_settings.param_options["MAXIMUM_AGE"] = "1000"
                    self.tracking_settings.current_options = {0: "DETECTION_THRESHOLD", 1: "MINIMUM_HITS", 2: "MAXIMUM_AGE", 3: ""}

                    return [
                        gr.Text(label="Detection threshold", value=str(self.tracking_settings.param_options["DETECTION_THRESHOLD"]), interactive=True, visible=False),
                        gr.Text(label="Minimum hits", value=str(self.tracking_settings.param_options["MINIMUM_HITS"]), interactive=True, visible=self.general_settings.advanced_view),
                        gr.Text(label="Maximum age", value=str(self.tracking_settings.param_options["MAXIMUM_AGE"]), interactive=True, visible=self.general_settings.advanced_view),
                        gr.Text(label="_", value='-', interactive=True, visible=False),
                    ]


class TrackerOption1Settings(ParamSetting):
    """
    Adjusts the first tracker option shown in the GUI. This can mean difference parameters for different trackers.
    """

    def __init__(self, general_settings: GeneralSettings, tracking_settings: TrackingSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters
        self.tracking_settings = tracking_settings

    def update(self, tracker_option_1: str):
        with self.locker.lock:
            try:
                float(tracker_option_1)
            except ValueError:
                print("Not a float")
                return
            if self.tracking_settings.current_options[0] == "":
                return
            if str(self.tracking_settings.param_options[self.tracking_settings.current_options[0]]):
                self.logger.info(f"Changed {self.tracking_settings.current_options[0]} from {str(self.tracking_settings.param_options[self.tracking_settings.current_options[0]])} to {str(tracker_option_1)}")
                self.tracking_settings.param_options[self.tracking_settings.current_options[0]] = tracker_option_1
                self.tracking_settings.reset = True


class TrackerOption2Settings(ParamSetting):
    """
    Adjusts the second tracker option shown in the GUI. This can mean difference parameters for different trackers.
    """

    def __init__(self, general_settings: GeneralSettings, tracking_settings: TrackingSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters
        self.tracking_settings = tracking_settings

    def update(self, tracker_option_2: str):
        with self.locker.lock:
            try:
                float(tracker_option_2)
            except ValueError:
                print("Not a float")
                return
            if self.tracking_settings.current_options[1] == "":
                return
            if str(self.tracking_settings.param_options[self.tracking_settings.current_options[1]]):
                self.logger.info(f"Changed {self.tracking_settings.current_options[1]} from {str(self.tracking_settings.param_options[self.tracking_settings.current_options[1]])} to {str(tracker_option_2)}")
                self.tracking_settings.param_options[self.tracking_settings.current_options[1]] = tracker_option_2
                self.tracking_settings.reset = True


class TrackerOption3Settings(ParamSetting):
    """
    Adjusts the third tracker option shown in the GUI. This can mean difference parameters for different trackers.
    """

    def __init__(self, general_settings: GeneralSettings, tracking_settings: TrackingSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters
        self.tracking_settings = tracking_settings

    def update(self, tracker_option_3: str):
        with self.locker.lock:
            try:
                float(tracker_option_3)
            except ValueError:
                print("Not a float")
                return
            if self.tracking_settings.current_options[2] == "":
                return
            if str(self.tracking_settings.param_options[self.tracking_settings.current_options[2]]):
                self.logger.info(f"Changed {self.tracking_settings.current_options[2]} from {str(self.tracking_settings.param_options[self.tracking_settings.current_options[2]])} to {str(tracker_option_3)}")
                self.tracking_settings.param_options[self.tracking_settings.current_options[2]] = tracker_option_3
                self.tracking_settings.reset = True


class TrackerOption4Settings(ParamSetting):
    """
    Adjusts the fourth tracker option shown in the GUI. This can mean difference parameters for different trackers.
    """

    def __init__(self, general_settings: GeneralSettings, tracking_settings: TrackingSettings, predictor_parameters: PredictorParameters, locker: Locker):
        super().__init__(locker)
        self.general_settings = general_settings
        self.predictor_parameters = predictor_parameters
        self.tracking_settings = tracking_settings

    def update(self, tracker_option_4: str):
        with self.locker.lock:
            try:
                float(tracker_option_4)
            except ValueError:
                print("Not a float")
                return
            if self.tracking_settings.current_options[3] == "":
                return
            if str(self.tracking_settings.param_options[self.tracking_settings.current_options[3]]):
                self.logger.info(f"Changed {self.tracking_settings.current_options[3]} from {str(self.tracking_settings.param_options[self.tracking_settings.current_options[3]])} to {str(tracker_option_4)}")
                self.tracking_settings.param_options[self.tracking_settings.current_options[3]] = tracker_option_4
                self.tracking_settings.reset = True
