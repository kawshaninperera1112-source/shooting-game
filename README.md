# 🎮 Python 3D Raycasting FPS

A retro first-person shooter in the style of *DOOM* and *Wolfenstein 3D*, written in **Python** with **Pygame**. The 3D view is rendered with a **raycasting** engine over a 2D tile map, and enemies hunt the player using **BFS pathfinding**.

> 📌 **Note:** This project is based on the open-source *"DOOM-style Game in Python"* tutorial series by Coder Space (StanislavPetrovV). I followed it to learn how raycasting engines work, then studied and modified the code. See [Credits](#-credits) and [My Changes](#-my-changes) below.

<!-- Replace with your own screenshot / GIF: -->
<!-- ![Gameplay](docs/gameplay.gif) -->

---

## 📖 Overview

You spawn in a maze-like level filled with **20 randomly placed enemies**. Find them, shoot them down with your shotgun, survive, and clear the level to win. If your health hits zero, the game restarts.

| | |
|---|---|
| **Genre** | 3D First-Person Shooter / Retro Raycaster |
| **Language** | Python 3 |
| **Library** | Pygame |
| **Techniques** | Raycasting (DDA), BFS pathfinding, sprite projection, animation state machines |

---

## ✨ Features

- **Raycasting renderer:** 640 rays across a 60° field of view, with textured walls, fisheye correction, and a scrolling sky.
- **Enemy AI:** NPCs use **Breadth-First Search** to find a route to the player, and a line-of-sight ray check to decide when to attack.
- **Three enemy types**, spawned randomly with weighted probability:

  | Enemy | Spawn weight | Health | Damage | Notes |
  |---|---|---|---|---|
  | 💂 Soldier | 70% | 100 | 10 | Ranged, standard enemy |
  | 👾 Caco Demon | 20% | 150 | 25 | Close-range, high accuracy |
  | 👹 Cyber Demon | 10% | 350 | 15 | Heavy, fast, long-range |

- **Shotgun weapon** with a shooting/reload animation and sound.
- **Health system:** on-screen health counter, blood-screen damage overlay, and slow health regeneration.
- **Sprites:** animated static objects (lights, candles) and animated NPC states (idle, walk, attack, pain, death).
- **Audio:** background music, weapon sounds, and enemy/player pain and death sounds.
- **Mouse look** with adjustable sensitivity.
- **Win / Game Over screens** with automatic restart.

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
- Pygame

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
pip install pygame
```

### Run the game

```bash
python main.py
```

> ⚠️ Run the command from inside the project folder, because assets are loaded using relative paths (`resources/...`).

---

## 🗂️ Project Structure

```
shooting-game/
├── main.py              # Game class, main loop, event handling
├── settings.py          # Resolution, FOV, player speed, mouse sensitivity, etc.
├── map.py               # Level layout (2D grid) and wall lookup
├── player.py            # Movement, mouse look, collision, health, shooting
├── raycasting.py        # Raycasting engine (DDA) and wall column rendering
├── object_renderer.py   # Textures, sky, floor, health display, overlays
├── object_handler.py    # Spawns and updates sprites and NPCs, win check
├── sprite_object.py     # Static and animated sprite projection
├── npc.py               # Enemy logic, animations, line-of-sight, combat
├── pathfinding.py       # BFS pathfinding graph for enemy movement
├── weapon.py            # Shotgun animation and damage
├── sound.py             # Music and sound effects
└── resources/           # Textures, sprites, and sounds
```

---

## 🧠 How It Works

### 1. Raycasting
For every vertical column of the screen, a ray is cast from the player at a slightly different angle. Using the **DDA (Digital Differential Analyzer)** algorithm, the ray steps from grid line to grid line until it hits a wall. The distance to the wall decides how tall the wall slice is drawn: closer walls are taller, distant walls are shorter. This turns a flat 2D map into a 3D-looking scene.

### 2. Sprite Projection
Enemies and objects are 2D images. Each frame, the game works out the angle and distance between the player and each sprite, projects it to a screen position, scales it by distance, and draws it in depth order together with the walls.

### 3. Enemy AI
- Each enemy casts its own ray toward the player to check **line of sight**.
- Once an enemy has seen the player, it uses **BFS** on the map grid to find the next tile on the shortest path and walks toward it.
- Within its attack distance, it stops and shoots with a per-enemy accuracy chance.

### 4. Animation
Sprites store their frames in a `deque` that is rotated on a timer, giving simple frame-by-frame animation for idle, walk, attack, pain, and death states.

---

## 🔧 My Changes

<!-- Fill this in with what YOU changed or added. Recruiters love this section. Examples: -->
- [ ] _e.g. Added crosshair, ammo and reload system_
- [ ] _e.g. Fixed frame-rate-dependent enemy speed_
- [ ] _e.g. Added a start menu and game states_

---

## 🛣️ Roadmap / Ideas

- [ ] Health and ammo pickups
- [ ] Crosshair and ammo counter (HUD)
- [ ] Main menu, pause menu, and game states
- [ ] Multiple levels and difficulty settings
- [ ] High-score saving
- [ ] Additional weapons
- [ ] Minimap
- [ ] Unit tests for pathfinding

---

## 🐛 Known Issues

- Frame rate is uncapped by default (`FPS = 0` in `settings.py`); set it to `60` to reduce CPU usage.
- Assets are loaded with relative paths, so the game must be launched from the project folder.
- The game freezes briefly (about 1.5 s) on the Win and Game Over screens.

---

## 🙏 Credits

- **Tutorial / base project:** [*DOOM-style Game in Python*](https://www.youtube.com/@CoderSpace) by Coder Space (StanislavPetrovV): the original raycasting FPS tutorial this project is based on.
- **Assets:** Textures, sprites, and sounds are used for **educational, non-commercial purposes** and belong to their original owners. Enemy designs are inspired by *DOOM* (id Software).
- Built with [Pygame](https://www.pygame.org/).

---

## 📄 License

Add a `LICENSE` file (for example, MIT) and mention it here. Note that third-party assets are **not** covered by this license.

---

## 👤 Author

**Kawshani Perera**
GitHub: [@kawshaninperera1112-source](https://github.com/kawshaninperera1112-source)
