from elements.model import ModelConfig
from elements.settings.params.advanced_view import AdvancedViewSetting
from elements.settings.params.architecture import ArchitectureSetting
from elements.settings.params.box_threshold import BoxThresholdSetting
from elements.settings.params.bpp import BPPSetting
from elements.settings.params.camera import CameraDimensionSetting, CameraIndexSetting
from elements.settings.params.camera_mode import CameraModeSetting
from elements.settings.params.classes import ClassesSetting
from elements.settings.params.device import DeviceSetting
from elements.settings.params.gamma_correction import GammaCorrectionBoolSetting, GammaCorrectionValueSetting
from elements.settings.params.input_height import InputHeightSetting
from elements.settings.params.input_width import InputWidthSetting
from elements.settings.params.normalize_type import NormalizeTypeSetting
from elements.settings.params.output_folder import OutputFolderSetting
from elements.settings.params.realistic_processing import RealisticProcessingSetting
from elements.settings.params.reset_stats_min import ResetStatsMinSetting
from elements.settings.params.save_frames import SaveAllFrames
from elements.settings.params.screen_dimension import ScreenDimensionSetting
from elements.settings.params.task_type import TaskTypeSetting
from elements.settings.params.tracked_classes import TrackedClassesSetting
from elements.settings.params.tracker import TrackerSetting, TrackerOption1Settings, TrackerOption2Settings, TrackerOption3Settings, TrackerOption4Settings
from elements.settings.params.weights import WeightsSetting


class SettingsOrchestrator:
    def __init__(self, model_manager):
        self.architecture_setting = ArchitectureSetting(general_settings=model_manager.general_settings, model_settings=model_manager.model_settings, config_parser=model_manager.config_parser, locker=model_manager.locker)
        self.weights_setting = WeightsSetting(general_settings=model_manager.general_settings, model_settings=model_manager.model_settings, config_parser=model_manager.config_parser, locker=model_manager.locker)

        self.task_type_setting = TaskTypeSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.tracked_classes_setting = TrackedClassesSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.classes_setting = ClassesSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)

        self.bpp_setting = BPPSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.gamma_correction_bool_setting = GammaCorrectionBoolSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.gamma_correction_value_setting = GammaCorrectionValueSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.input_height_setting = InputHeightSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.input_width_setting = InputWidthSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)

        self.device_setting = DeviceSetting(model_settings=model_manager.model_settings, locker=model_manager.locker)

        self.advanced_view_setting = AdvancedViewSetting(general_settings=model_manager.general_settings, tracking_settings=model_manager.tracking_settings, locker=model_manager.locker)
        self.realistic_processing_setting = RealisticProcessingSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.screen_dimension_setting = ScreenDimensionSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)

        self.camera_dimension_setting = CameraDimensionSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.camera_index_setting = CameraIndexSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.reset_stats_min = ResetStatsMinSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.save_all_frames_setting = SaveAllFrames(general_settings=model_manager.general_settings, locker=model_manager.locker)

        self.box_threshold_setting = BoxThresholdSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)

        self.tracker_setting = TrackerSetting(general_settings=model_manager.general_settings, tracking_settings=model_manager.tracking_settings, locker=model_manager.locker)
        self.tracker_option_1_setting = TrackerOption1Settings(general_settings=model_manager.general_settings, tracking_settings=model_manager.tracking_settings, locker=model_manager.locker)
        self.tracker_option_2_setting = TrackerOption2Settings(general_settings=model_manager.general_settings, tracking_settings=model_manager.tracking_settings, locker=model_manager.locker)
        self.tracker_option_3_setting = TrackerOption3Settings(general_settings=model_manager.general_settings, tracking_settings=model_manager.tracking_settings, locker=model_manager.locker)
        self.tracker_option_4_setting = TrackerOption4Settings(general_settings=model_manager.general_settings, tracking_settings=model_manager.tracking_settings, locker=model_manager.locker)

        self.camera_mode_setting = CameraModeSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.output_folder_setting = OutputFolderSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)
        self.normalize_type_setting = NormalizeTypeSetting(general_settings=model_manager.general_settings, locker=model_manager.locker)

    def initialize_values(self, config: ModelConfig):
        self.task_type_setting.update(task_type=config.task_type)  # This has to go first as the others depend on it

        self.architecture_setting.update(architecture=config.architecture)
        self.weights_setting.update(weights_path=config.weights)

        self.normalize_type_setting.update(normalize_type=config.normalize_type)
        self.classes_setting.update(classes=config.classes)
        self.tracked_classes_setting.update(classes=config.tracked_classes)
        self.bpp_setting.update(bpp=config.bpp)
        self.input_height_setting.update(input_height=config.input_height)
        self.input_width_setting.update(input_width=config.input_width)
        self.box_threshold_setting.update(box_threshold=config.box_threshold)
        self.tracker_setting.update(tracker=config.tracker)
