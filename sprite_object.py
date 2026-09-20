import math
import os
from collections import deque

import pygame as pg

from settings import DELTA_ANGLE, HALF_HEIGHT, HALF_NUM_RAYS, SCALE, SCREEN_DIST, WIDTH

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp')

# Images are loaded from disk only once and shared, so restarting the game is instant.
_image_cache = {}
_frames_cache = {}


def load_image(path):
    """Load an image (once) and return the cached Surface. Never modify the result in place."""
    image = _image_cache.get(path)
    if image is None:
        image = _image_cache[path] = pg.image.load(path).convert_alpha()
    return image


def _frame_sort_key(file_name):
    """Sort '0.png, 1.png ... 10.png' numerically (plain sorting would put 10 before 2)."""
    stem = os.path.splitext(file_name)[0]
    return (0, int(stem), '') if stem.isdigit() else (1, 0, stem)


def load_frames(folder):
    """Return the animation frames in `folder` as a NEW deque (each sprite rotates its own copy)."""
    frames = _frames_cache.get(folder)
    if frames is None:
        file_names = [f for f in os.listdir(folder)
                      if f.lower().endswith(IMAGE_EXTENSIONS) and os.path.isfile(os.path.join(folder, f))]
        file_names.sort(key=_frame_sort_key)
        frames = _frames_cache[folder] = [load_image(os.path.join(folder, f)) for f in file_names]
    return deque(frames)


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = load_image(path)
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (int(proj_width), int(proj_height)))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        return load_frames(path)