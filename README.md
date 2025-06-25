# 2025-major-work
wallace's lovely major work
# Maths Defence

A 2D tower defence game written in [Pygame](https://www.pygame.org/) for a school major work.  You defend your base by placing towers that defeat incoming enemies.  Each level introduces different enemy waves and background music.

## Repository layout

```
pygame major project 2D tower defence by wallace/
├── assets/   # game images
├── audio/    # sound effects and music
├── classes/  # Enemy, Tower, Attack and Button implementations
├── config.py           # game constants and level presets
├── ingame_level_data.py  # runtime data storage
├── main.py             # game entry point
└── test.py             # misc test script
```

The `config.py` file defines `Initialise`, `Level_preset` and `Tower_preset` dictionaries which hold most of the game data such as images, sound paths, tower statistics and level configuration.

## Requirements

- Python 3.9 or newer
- `pygame` 2.x

## Installation

1. Download this repository.
2. run main .exe
3. (optional) right click main .exe and create a shortcut for it on desktop


Use your mouse to navigate the menus and place towers.  The pause and home buttons are accessible during gameplay.  Progress through the tutorial and five levels to win the game.

## Notes

All media files used by the game are located inside the `assets/` and `audio/` folders.  The game window is resizable and most positions and scales are derived from the base resolution defined in `config.py`.

Enjoy defending your base!
