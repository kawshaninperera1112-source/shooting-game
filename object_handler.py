from random import choices, randrange

from npc import CacoDemonNPC, CyberDemonNPC, SoldierNPC
from settings import ENEMY_WEIGHTS, NUM_ENEMIES, STATE_WIN
from sprite_object import AnimatedSprite

GREEN_LIGHT_POSITIONS = [
    (11.5, 3.5), (1.5, 1.5), (1.5, 7.5), (5.5, 3.25), (5.5, 4.75), (7.5, 2.5), (7.5, 5.5),
    (14.5, 1.5), (14.5, 4.5), (14.5, 24.5), (14.5, 30.5), (1.5, 30.5), (1.5, 24.5),
]
RED_LIGHT_POSITIONS = [
    (14.5, 5.5), (14.5, 7.5), (12.5, 7.5), (9.5, 7.5), (14.5, 12.5),
    (9.5, 20.5), (10.5, 20.5), (3.5, 14.5), (3.5, 18.5),
]


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = set()   # tiles occupied by living NPCs

        # spawn npc
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = ENEMY_WEIGHTS
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # no spawns near the player
        self.spawn_npc()

        # decorative sprites
        for pos in GREEN_LIGHT_POSITIONS:
            self.add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'green_light/0.png', pos=pos))
        for pos in RED_LIGHT_POSITIONS:
            self.add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=pos))

    def spawn_npc(self):
        occupied = set()
        for _ in range(NUM_ENEMIES):
            npc_type = choices(self.npc_types, self.weights)[0]
            pos = self.random_free_tile(occupied)
            occupied.add(pos)
            x, y = pos
            self.add_npc(npc_type(self.game, pos=(x + 0.5, y + 0.5)))

    def random_free_tile(self, occupied):
        """Pick a random floor tile that is not a wall, not near the player and not already used."""
        while True:
            pos = randrange(self.game.map.cols), randrange(self.game.map.rows)
            if (pos not in self.game.map.world_map and pos not in self.restricted_area
                    and pos not in occupied):
                return pos

    def handle_shot(self):
        """Resolve the player's shot: only the closest enemy under the crosshair is hit."""
        player = self.game.player
        if not player.shot:
            return
        player.shot = False
        targets = [npc for npc in self.npc_list if npc.is_targeted()]
        if targets:
            min(targets, key=lambda npc: npc.dist).take_hit(self.game.weapon.damage)

    def check_win(self):
        if not any(npc.alive for npc in self.npc_list):
            self.game.set_state(STATE_WIN)

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()
        self.handle_shot()
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)