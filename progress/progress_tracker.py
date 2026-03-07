"""
Progress tracking system
Allows pipeline to resume after crash or Colab reset
"""

import json
import os


class ProgressTracker:

    def __init__(self, file_path="progress_state.json"):
        self.file_path = file_path
        self.state = self.load_progress()

    def load_progress(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def save_progress(self):
        with open(self.file_path, "w") as f:
            json.dump(self.state, f, indent=2)

    def mark_step_done(self, video_id, step_name):

        if video_id not in self.state:
            self.state[video_id] = {}

        self.state[video_id][step_name] = True
        self.save_progress()

    def is_step_done(self, video_id, step_name):

        return (
            video_id in self.state
            and step_name in self.state[video_id]
            and self.state[video_id][step_name]
        )

    def reset_video(self, video_id):

        if video_id in self.state:
            del self.state[video_id]
            self.save_progress()
