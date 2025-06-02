# 3D Vivarium: Predator-Prey Simulation
## Project Overview
A 3D simulated ecosystem featuring:
- **Predator model**: Bird with flapping wings
- **Prey model**: Mouse with wagging tail
- **Collision detection**: Wall avoidance and predator-prey interactions
- **Behavior systems**: Chase/evade mechanics using potential functions

## Model Components

### Predator (Bird)
- Flapping wings animation
- Chase behavior using potential functions
- Collision detection with walls

### Prey (Mouse)
- Wagging tail animation
- Evasion behavior
- Disappears when captured

## Controls

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| R   | Reset entire vivarium |
| T   | Test scene (1 predator + 1 prey) |
| ESC | Exit selection mode |

### Mouse Controls
| Action | Function |
|--------|----------|
| Left Drag | Orbit camera |
| Middle Drag | Pan camera |
| Scroll Wheel | Zoom in/out |

## Installation
```bash
# 1. Create conda environment
conda env create -n graphics -f environment.yml

# 2. Activate environment
conda activate graphics

# 3. Run the simulation
python Sketch.py

```

## Known Issues

- Occasional clipping through walls at high speeds
- Multi-selection mode conflicts with single selection
- Camera sensitivity varies by input device

## Academic Note

Original framework by micou (Zezhou Sun).

Behavior systems and creative models implemented by Brian Shaw for PC 400 Assignment 9

Collaborated with Thomas Quan and Aparna Singh