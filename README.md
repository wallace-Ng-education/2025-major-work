# 2025-major-work
wallace's lovely major work
More info on [https://sites.google.com/education.nsw.gov.au/
wallaceng2025semwwebsite](url)
# Maths Defence

A 2D tower defence game written in [Pygame](https://www.pygame.org/) for a school major work.  You defend your base by placing towers that defeat incoming enemies.  Each level introduces different enemy waves and background music.

## Requirements

- System storage of minimum 43.4MB

## Installation

1. Download that respository as a zip file.
2. Extract the zip file
3. Run / Double-tap main .exe , which locates in 2025-major-work-main\pygame major project 2D tower defence by wallace\main .exe" of the unzipped file.
4. Optional: create a shortcut for main .exe on desktop for efficient access.

## How to play - basics

Use your mouse to navigate the menus and place towers.  The pause and home buttons are accessible during gameplay.  Progress through the tutorial and five levels to win the game.

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

## Notes

All media files used by the game are located inside the `assets/` and `audio/` folders.  The game window is resizable and most positions and scales are derived from the base resolution defined in `config.py`.

Enjoy defending your base!
