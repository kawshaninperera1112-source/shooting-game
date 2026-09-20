import math

# --- display ---
RES = WIDTH, HEIGHT = 1280, 722
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60                # frame-rate cap (0 would mean "unlimited")
MAX_DELTA_MS = 50       # longest frame time used for movement (avoids huge jumps after a stall)
CAPTION = 'Python 3D Raycasting FPS'

# --- player ---
PLAYER_POS = 1.5, 5     # starting position (in map tiles)
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100
PLAYER_HEALTH_RECOVERY_DELAY = 700   # ms between +1 health

# --- mouse ---
MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# --- rendering ---
FLOOR_COLOR = (30, 30, 30)
DAMAGE_FLASH_MS = 120   # how long the blood overlay stays on screen

# --- raycasting ---
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 40          # must be >= the longest straight line through the map
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# --- enemies ---
NUM_ENEMIES = 20
ENEMY_WEIGHTS = [70, 20, 10]          # Soldier, CacoDemon, CyberDemon spawn chances (%)
NPC_REFERENCE_FRAME_MS = 1000 / 60    # NPC speeds below are "tiles per 60 FPS frame"

# --- game flow ---
STATE_PLAYING = 'playing'
STATE_WIN = 'win'
STATE_GAME_OVER = 'game_over'
END_SCREEN_MS = 1500    # how long the win / game-over screen stays before restarting