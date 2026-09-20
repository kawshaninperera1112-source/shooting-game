import pygame as pg


class _SilentSound:
    """Stand-in used when a sound (or the audio device) is unavailable, so the game still runs."""

    def play(self, *args, **kwargs):
        pass


class Sound:
    def __init__(self, game):
        self.game = game
        self.path = 'resources/sound/'
        try:
            pg.mixer.init()
        except pg.error:
            print('Warning: no audio device found, running without sound.')

        self.shotgun = self.load_sound('shotgun.wav')
        self.npc_pain = self.load_sound('npc_pain.wav')
        self.npc_death = self.load_sound('npc_death.wav')
        self.npc_shot = self.load_sound('npc_attack.wav')
        self.player_pain = self.load_sound('player_pain.wav')

        self.music_ready = False
        try:
            pg.mixer.music.load(self.path + 'theme.mp3')
            pg.mixer.music.set_volume(0.3)
            self.music_ready = True
        except (pg.error, FileNotFoundError):
            print('Warning: could not load the background music.')

    def load_sound(self, file_name):
        try:
            return pg.mixer.Sound(self.path + file_name)
        except (pg.error, FileNotFoundError):
            print(f'Warning: could not load sound "{file_name}".')
            return _SilentSound()

    def play_music(self):
        if self.music_ready:
            pg.mixer.music.play(-1)
