from elements.trackers.tracker_processor import TrackerProcessor


class GeneralizedProcessor(TrackerProcessor):
    def update_tracks(self, active_tracks: list, verbose: bool = True) -> bool:
        """
        Uses the custom Track objects to keep a list of which instances have been counted already.
        """
        save_image: bool = False
        for track in active_tracks:
            if track.track_id not in self.tracks.keys():
                if verbose:
                    self.logger.info(f"{self.general_settings.classes[int(track.class_id)]} added")
                self.tracks[track.track_id] = {"passed": True}
                self.counts[self.general_settings.classes[int(track.class_id)]] += 1
                save_image = True
                continue
        return save_image
