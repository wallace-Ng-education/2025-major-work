# 2025-major-work
wallace's lovely major work.

More info on https://sites.google.com/education.nsw.gov.au/wallaceng2025semwwebsite

# Maths Defence

A 2D tower defence game written in [Pygame](https://www.pygame.org/) for a school major work.  You defend your base by placing towers that defeat incoming enemies.  Each level introduces different enemy waves and background music.


## Requirements- Windows

- System storage of minimum 43.4MB
- 64-bit Windows operating system
- 
## Installation - Windows

1. Download that respository as a zip file.
2. Extract the zip file
3. Run / Double-tap main.exe , which locates at 2025-major-work-main\pygame major project 2D tower defence by wallace\main.exe" of the unzipped file.
4. Optional: create a shortcut for main.exe on desktop for efficient access.
5. Optional: Feedback after playing would be really appreciated! https://docs.google.com/forms/d/e/1FAIpQLSdY0cxqxB_DfHvy_72U16Gi22e6Tk_y4nVFeBIMJpfaTCJAiQ/viewform?usp=dialog

## Requirements- Mac

- System storage of minimum 43.4MB
- macOS - Ventura or above
- Python - v 3.1 or above


## Installation - Mac

1. Download that respository as a zip file.
2. Extract the zip file
3. Download pip (type "python3 get-pip.py" in terminal)
4. Download pygame (type "pip3 install pygame" in terminal)
5. Run main.py , which locates at 2025-major-work-main\pygame major project 2D tower defence by wallace\main.py" of the unzipped file. (locate the file location and then type "python3 main.py" in terminal)
6. Optional: Feedback after playing would be really appreciated! https://docs.google.com/forms/d/e/1FAIpQLSdY0cxqxB_DfHvy_72U16Gi22e6Tk_y4nVFeBIMJpfaTCJAiQ/viewform?usp=dialog


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
