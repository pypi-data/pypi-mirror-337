class LanguagePreferences:
    def __init__(self):
        self.playback = None
        self.subtitle = None
        self.subs_enabled = None
        self.app = None

    def __str__(self):
        return self.app
