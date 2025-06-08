import pygame

# list for enemies spawned and are still on the screen
Enemy_list = pygame.sprite.Group()
# list for enemies prepared to spawn
Enemy_prep_list: list = []
#
Enemy_dead_list = pygame.sprite.Group()
# list of attacks
Attack_list = pygame.sprite.Group()
# list of towers
Tower_list = pygame.sprite.Group()
# list of Button items
Shop_item_list: list = []
Button_list: list = []
Rect_list: list = []
Dialogue_list: list = []

Ingame_data = {
        "current_player_health": None,
        "current_player_currency": None,
        "held_item": None,
        "tower_placed": 0,

        "Enemy_list": Enemy_list,
        "Enemy_prep_list": Enemy_prep_list,
        "Enemy_dead_list": Enemy_dead_list,
        "Attack_list": Attack_list,
        "Tower_list": Tower_list,
        "Shop_item_list" : Shop_item_list,
        "Button_list": Button_list,
        "Rect_list": Rect_list,
        "Dialogue_list": Dialogue_list,

        # resize factor of 1 means no change in sie
        "resize_factor": 1,
        "checkpoints": [],
        "enemy_count": 0,
        
        "time_level_init": None,
        "time_paused": 0,

        "running": False,
        "level_selected": None,
        "level_running": None
}