from elements.settings.general_settings import GeneralSettings
from elements.settings.tracking_settings import TrackingSettings
from elements.trackers.general import GeneralizedProcessor


class TrackerFactory:
    @staticmethod
    def create(general_settings: GeneralSettings, tracking_settings: TrackingSettings):
        tracker_model = tracking_settings.tracker_generator(min_hits=int(tracking_settings.param_options["MINIMUM_HITS"]),
                                          max_age=int(tracking_settings.param_options["MAXIMUM_AGE"]),
                                          det_thresh=float(general_settings.box_threshold))
        tracker_processor = GeneralizedProcessor(general_settings=general_settings,
                                                 min_hits=int(tracking_settings.param_options["MINIMUM_HITS"]),
                                                 tracker=tracker_model)
        return tracker_model, tracker_processor