from elements.trackers.tracker import Tracker
import gradio as gr


class GeneralizedProcessor(Tracker):
    def update_tracks(self, active_tracks: list, verbose: bool = True) -> bool:
        """
        Uses the custom Track objects to keep a list of which instances have been counted already
        """
        save_image = False
        for track in active_tracks:
            if track.track_id not in self.tracks.keys():
                if verbose:
                    gr.Info(f"{self.general_settings.classes[int(track.class_id)]} added", duration=1)
                self.tracks[track.track_id] = {"passed": True}
                self.counts[self.general_settings.classes[int(track.class_id)]] += 1
                save_image = True
                continue
        return save_image
