import pygame
pygame.init()


screen = pygame.display.set_mode((940, 540), pygame.RESIZABLE)
# convert to make it load more quickly, alpha allows image transparency
enemy_snakeIMG = pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_snakeIMG.png').convert_alpha(), 1.5)
bullet_IMG = pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/attack_linearIMG.png').convert_alpha(), 0.7)
tower_testIMG = pygame.image.load('pygame major project 2D tower defence by wallace/assets/tower_test.png').convert()

# text font initialise
enemy_health_font = pygame.font.SysFont("cambria", 25, False, False)
player_health_font = pygame.font.SysFont("cambria", 20, True, False)
player_currency_font = pygame.font.SysFont("cambria", 20, True, False)

# frames per second

fps = 30

Level_preset = {
    # 1
    "level1": {
        "enemy_data": {
            "snake": {
                "health": 200,
                # distance in pixels
                "distance_per_second": 100,
                "image": enemy_snakeIMG,
                "spawn_time": (),
                "bounty": 10
            },
            "ant_g": {
                "health": 100,
                # distance in pixels
                "distance_per_second": 100,
                "image": enemy_snakeIMG,
                "spawn_time": (3.4, 4.5, 6, 1, 2, 3, 5, 7, 8, 9, 10),
                "bounty": 5
            }
        },
        "background_image": pygame.image.load('pygame major project 2D tower defence by wallace/assets/level1_background.png'),
        "checkpoints": [(0, 0), (260, 180), (120, 300), (300, 400), (530, 230), (710, 350), (570, 470), (700, 570)],
        "player_health": 100,
        "player_currency": 100,
    },

    # 2
    "level2": {}
}
