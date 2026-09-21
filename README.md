# 🎮 Python 3D Raycasting FPS

A retro first-person shooter in the style of *DOOM* and *Wolfenstein 3D*, written in **Python** with **Pygame**. The 3D view is rendered with a **raycasting** engine over a 2D tile map, and enemies hunt the player using **BFS pathfinding**.

> 📌 **Note:** This project is based on the open-source *"DOOM-style Game"* project and video tutorial by Coder Space (StanislavPetrovV). I followed it to learn how raycasting engines work, then studied the code, fixed bugs, and improved it. See [My Changes](#-my-changes) and [Credits](#-credits).


🎬 Demo

▶️ Watch the gameplay video

<video src="https://github.com/kawshaninperera1112-source/shooting-game/raw/main/shooting%20game.mp4" controls muted width="100%"> Your browser does not support the video tag. Use the link above to watch the gameplay. </video>

---

## 📖 Overview

You spawn in a maze-like level filled with **20 randomly placed enemies**. Find them, shoot them down with your shotgun, survive, and clear the level to win. If your health hits zero, the game shows a Game Over screen and restarts.

| | |
|---|---|
| **Genre** | 3D First-Person Shooter / Retro Raycaster |
| **Language** | Python 3 |
| **Library** | Pygame |
| **Techniques** | Raycasting (DDA), BFS pathfinding, sprite projection, animation state machines, game states |

---

## ✨ Features

- **Raycasting renderer:** 640 rays across a 60° field of view, textured walls, fisheye correction, and a scrolling sky.
- **Enemy AI:** NPCs use **Breadth-First Search** to find a route to the player, and a line-of-sight ray check to decide when to attack.
- **Three enemy types**, spawned randomly with weighted probability:

  | Enemy | Spawn weight | Health | Damage | Notes |
  |---|---|---|---|---|
  | 💂 Soldier | 70% | 100 | 10 | Ranged, standard enemy |
  | 👾 Caco Demon | 20% | 150 | 25 | Close-range, high accuracy |
  | 👹 Cyber Demon | 10% | 350 | 15 | Heavy, fast, long-range |

- **Shotgun weapon** with a shooting/reload animation and sound. A shot hits the **closest enemy under the crosshair**.
- **Health system:** on-screen health counter, blood-flash damage overlay, and slow health regeneration.
- **Game states:** Playing → Win / Game Over screen → automatic restart (the window never freezes; `ESC` always works).
- **Audio:** background music, weapon sounds, enemy/player pain and death sounds. The game still runs if no audio device is available.
- **Mouse look** with adjustable sensitivity, and a 60 FPS frame cap.

---

## 🕹️ Controls

| Action | Input |
|---|---|
| Move forward / backward | `W` / `S` |
| Strafe left / right | `A` / `D` |
| Look around | Mouse movement |
| Shoot | Left mouse button |
| Quit | `ESC` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or newer

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/kawshaninperera1112-source/shooting-game.git
cd shooting-game

# 2. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the game

```bash
python main.py
```

Settings such as resolution, FPS cap, mouse sensitivity, enemy count, and player speed can be changed in `settings.py`.

---

## 🗂️ Project Structure

```
shooting-game/
├── main.py              # Game class, main loop, game states (playing / win / game over)
├── settings.py          # All constants: resolution, FPS, FOV, speeds, enemy count, ...
├── map.py               # Level layout (2D grid) and wall lookup
├── player.py            # Movement, mouse look, collision, health, shooting
├── raycasting.py        # Raycasting engine (DDA) and wall column rendering
├── object_renderer.py   # Textures, sky, floor, health display, damage overlay
├── object_handler.py    # Spawns and updates sprites and NPCs, resolves shots, win check
├── sprite_object.py     # Static and animated sprites, cached image loading
├── npc.py               # Enemy logic, animations, line-of-sight, combat
├── pathfinding.py       # BFS pathfinding for enemy movement
├── weapon.py            # Shotgun animation and damage
├── sound.py             # Music and sound effects
├── requirements.txt     # Python dependencies
└── resources/           # Textures, sprites, and sounds
```

---

## 🧠 How It Works

### 1. Raycasting
For every vertical column of the screen, a ray is cast from the player at a slightly different angle. Using the **DDA (Digital Differential Analyzer)** algorithm, the ray steps from grid line to grid line until it hits a wall. The distance to the wall decides how tall that wall slice is drawn: closer walls are taller, distant walls are shorter. This turns a flat 2D map into a 3D-looking scene.

### 2. Sprite Projection
Enemies and objects are 2D images. Each frame, the game works out the angle and distance between the player and each sprite, projects it to a screen position, scales it by distance, and draws it in depth order together with the walls.

### 3. Enemy AI
- Each enemy casts its own ray toward the player to check **line of sight**.
- Once an enemy has seen the player, it follows the shortest path to the player. A single **BFS** runs outward from the player's tile, giving every tile a pointer to the next step toward the player. All enemies share that result, and it is recomputed only when the player moves to a new tile.
- Within its attack distance, an enemy stops and shoots, with a per-enemy accuracy chance.
- Enemy movement is scaled by the real frame time, so speed is the same on fast and slow computers.

### 4. Shooting
When the player fires, every enemy that is visible and under the crosshair is a candidate, and only the **closest** one takes damage.

### 5. Animation
Sprites store their frames in a `deque` that is rotated on a timer, giving simple frame-by-frame animation for idle, walk, attack, pain, and death states. Images are loaded from disk once and cached, so restarting a round is instant.

---

## 🔧 My Changes

Starting from the tutorial code, I found and fixed these problems:

- **Frame-rate cap:** the game ran with an unlimited FPS (`FPS = 0`), using 100% CPU and risking a division by zero. It is now capped at 60 FPS, and very long frames are clamped so nothing can jump through walls.
- **Frame-rate-independent enemies:** enemy speed now depends on real elapsed time, not on how many frames per second the computer renders.
- **Correct shot targeting:** a shot used to hit whichever enemy happened to be first in the list. It now hits the closest enemy under the crosshair.
- **Animation order:** animation frames are sorted numerically, so `10.png` no longer plays before `2.png`, and behaviour is the same on every operating system.
- **Pathfinding:** replaced the `lru_cache` (which could return outdated paths) with one BFS from the player, cached until the player changes tile. Also stopped enemies from cutting diagonally through wall corners.
- **Game states:** replaced `pg.time.delay()` (which froze the window) with proper Playing / Win / Game Over states, and stopped enemies from damaging the player after death.
- **Faster restarts:** textures, sprites, and sounds are loaded once and cached; the music no longer restarts every round.
- **Robustness:** `MAX_DEPTH` raised from 20 to 40 (the map is 32 tiles tall), divide-by-zero guards in raycasting, the game works from any working directory, and it keeps running without an audio device or a missing sound file.
- **Spawning:** two enemies can no longer spawn on the same tile.
- **Code quality:** explicit imports instead of `import *`, unused and debug code removed, constants moved to `settings.py`, docstrings added, and the blood overlay now shows for a fixed time.

---

## 🛣️ Roadmap / Ideas

- [ ] Health and ammo pickups
- [ ] Crosshair and ammo counter (HUD)
- [ ] Main menu and pause menu
- [ ] Multiple levels and difficulty settings
- [ ] High-score saving
- [ ] Additional weapons
- [ ] Minimap
- [ ] Unit tests for pathfinding

---

## 🐛 Known Limitations

- Only one level, and it is defined directly in `map.py`.
- Enemies wait if the next tile on their path is occupied by another enemy, instead of walking around them.
- There is no ammo limit, HUD crosshair, or pause menu yet (see Roadmap).

---

## 🙏 Credits

- **Base project:** [StanislavPetrovV/DOOM-style-Game](https://github.com/StanislavPetrovV/DOOM-style-Game) and the video tutorial *"Creating a DOOM (Wolfenstein)-style 3D Game in Python"* by Coder Space. The engine structure (raycasting, sprites, NPC logic) comes from this tutorial.
- **Assets:** Textures, sprites, and sounds are used for **educational, non-commercial purposes** and belong to their original owners. Enemy designs are inspired by *DOOM* (id Software).
- Built with [Pygame](https://www.pygame.org/).

---

## 📄 License

No license has been chosen yet. Because this project is built on the tutorial repository above, check that repository's license terms before adding a `LICENSE` file here. Third-party assets (textures, sprites, sounds) are **not** covered by any license I could grant.

---

## 👤 Author

**kawshani Perera**
GitHub: [@kawshaninperera1112-source](https://github.com/kawshaninperera1112-source)
