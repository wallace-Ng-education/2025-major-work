import pygame
import config

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


Ingame_data = {
        "current_player_health": 100,
        "current_player_currency": 100,
        "Enemy_list": Enemy_list,
        "Enemy_prep_list": Enemy_prep_list,
        "Enemy_dead_list": Enemy_dead_list,
        "Attack_list": Attack_list,
        "Tower_list": Tower_list,
}
