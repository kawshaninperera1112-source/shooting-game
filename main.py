import os
import sys

import pygame as pg

from map import Map
from object_handler import ObjectHandler
from object_renderer import ObjectRenderer
from pathfinding import PathFinding
from player import Player
from raycasting import RayCasting
from settings import (CAPTION, END_SCREEN_MS, FPS, MAX_DELTA_MS, RES, STATE_GAME_OVER, STATE_PLAYING,
                      STATE_WIN)
from sound import Sound
from weapon import Weapon

# Assets are loaded with relative paths ('resources/...'), so always run from this file's folder.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption(CAPTION)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.state = STATE_PLAYING
        self.state_start = 0
        self.sound = Sound(self)     # loaded once and reused on every restart
        self.sound.play_music()
        self.new_game()

    def new_game(self):
        self.state = STATE_PLAYING
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)

    def set_state(self, state):
        """Switch from PLAYING to WIN / GAME_OVER (ignored if the round has already ended)."""
        if self.state == STATE_PLAYING:
            self.state = state
            self.state_start = pg.time.get_ticks()

    def update(self):
        if self.state == STATE_PLAYING:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
        elif pg.time.get_ticks() - self.state_start >= END_SCREEN_MS:
            self.new_game()   # end screen was shown long enough: start a fresh round

    def draw(self):
        if self.state == STATE_WIN:
            self.object_renderer.win()
        elif self.state == STATE_GAME_OVER:
            self.object_renderer.game_over()
        else:
            self.object_renderer.draw()
            self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            pg.display.flip()
            self.delta_time = min(max(1, self.clock.tick(FPS)), MAX_DELTA_MS)
            pg.display.set_caption(f'{CAPTION} - {self.clock.get_fps():.0f} FPS')


if __name__ == '__main__':
    game = Game()
    game.run()