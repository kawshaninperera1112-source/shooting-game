# 🎮 Python 3D Raycasting FPS Game

This is a classic 3D First-Person Shooter (FPS) game built from scratch using **Python** and **Pygame**, utilizing the **Raycasting algorithm** (similar to DOOM and Wolfenstein 3D).

---

## 🕹️ Game Overview (ගේම් එක ගැන විස්තරය)

* **Genre:** 3D First-Person Shooter (FPS) / Retro Raycaster
* **Language:** Python
* **Graphics Library:** Pygame
* **Mechanics:** Raycasting engine, DDA algorithm, BFS Pathfinding for AI, Animated Sprites, Sound Effects.

### 📝 Short Description
In this game, players navigate through a maze-like 3D environment generated using 2D raycasting technique. Fight off different types of enemies (Soldiers, Caco Demons, and Cyber Demons) using your shotgun, manage your health, and clear all enemies to win the game!

---

## ✨ Key Features (ප්‍රධාන විශේෂාංග)

* **3D Raycasting Engine:** Custom-built rendering engine to simulate a 3D environment using 2D maps.
* **Smart NPC AI:** Enemies utilize **BFS (Breadth-First Search) pathfinding** to track and hunt down the player.
* **Multiple Enemy Types:** 
  * 💂 **Soldier NPC:** Standard ranged enemy.
  * 👾 **CacoDemon NPC:** Fast melee/close-range enemy with high health.
  * 👹 **CyberDemon NPC:** Heavy boss enemy with high damage output.
* **Dynamic Weapon System:** Interactive shotgun with shooting animations and audio effects.
* **Audio System:** Background music, directional shooting sounds, enemy pain/death sounds, and damage audio feedback.
* **Dynamic Sky & Textures:** Wall textures, blood splatter damage overlay, and interactive mouse-look camera support.

---

## 🎮 Game Controls (ගේම් එක Play කරන හැටි)

| Action | Key / Input |
| :--- | :--- |
| **Move Forward / Backward** | `W` / `S` |
| **Strafe Left / Right** | `A` / `D` |
| **Aim / Look Around** | `Mouse Movement` |
| **Shoot Weapon** | `Left Mouse Click` |
| **Quit Game** | `ESC` |

---

## 🚀 Getting Started (Run කරන්නේ කොහොමද?)

### Prerequisites
Make sure you have **Python 3.x** and **Pygame** installed on your system.

```bash
pip install pygame
