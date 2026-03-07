"""
Subtitle Styles
Defines subtitle styling presets
"""


class SubtitleStyles:

    @staticmethod
    def tiktok():

        return {
            "font": "Arial-Bold",
            "fontsize": 64,
            "color": "white",
            "border_color": "black",
            "border_width": 3,
            "position": "bottom",
            "highlight_color": "yellow"
        }

    @staticmethod
    def mrbeast():

        return {
            "font": "Impact",
            "fontsize": 72,
            "color": "white",
            "border_color": "black",
            "border_width": 4,
            "position": "center",
            "highlight_color": "yellow"
        }

    @staticmethod
    def podcast():

        return {
            "font": "Arial",
            "fontsize": 48,
            "color": "white",
            "border_color": "black",
            "border_width": 2,
            "position": "bottom",
            "highlight_color": "none"
        }
