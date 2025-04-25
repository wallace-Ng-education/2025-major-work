import pygame
pygame.init()


Initialise = {
    # screen, icon and title
    "screen_size" : (940, 540),
    "screen" : pygame.display.set_mode((940,540), pygame.RESIZABLE),
    "icon" : 'pygame major project 2D tower defence by wallace/assets/game-icon.png',
    "title" : "Maths defence",

    # convert to make it load more quickly, alpha allows image transparency
    "enemy_snakeIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_snakeIMG.png').convert_alpha(), 1.3),
    "bullet_IMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/attack_linearIMG.png').convert_alpha(), 0.7),
    "tower_testIMG" : pygame.image.load('pygame major project 2D tower defence by wallace/assets/tower_test.png').convert(),
    #"shop_itemIMG: pygame.image.load

    # text font initialise
    # consider importing settings to a list that fit into pygame.font.SysFont() -> usually [text family: str, size: int, blod: bool, i]
    "enemy_health_font" : ["cambria", 25, False, False],
    "player_health_font" : ["cambria", 20, True, False],
    "player_currency_font" : ["cambria", 20, True, False],

    # frames per second
    "fps" : 30
}

Level_preset = {
    # home screen
    "home": { # rect[85 + 285k, 70 + 235m, 200, 200 ]  -- > k and m are integers 
              # k represents the column number, m the row number
        "rect":{
            "tutorial": {
                "cords": [85, 70, 200, 200],
                "color": (0, 255, 0),
                },
            "level1": {
                "cords": [370, 70, 200, 200],
                "color": (0, 0, 0),
                },
        },
    },

    # 1
    "level1": {
        "enemy_data": {
            "snake": {
                "health": 200,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_snakeIMG"],
                "spawn_time": (tuple([x for x in range(10, 10000)])),
                "bounty": 30
            },
            "ant_g": {
                "health": 100,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_snakeIMG"],
                "spawn_time": {1, 2,3,4,5,6,7,8,9,20}, # (tuple([x/100 for x in range(1000)])),
                "bounty": 15
            }
        },
        "background_image": pygame.image.load('pygame major project 2D tower defence by wallace/assets/level1_background.png'),
        "checkpoints": [(0, 0), (260, 180), (120, 300), (300, 400), (530, 230), (710, 350), (570, 470), (700, 570)],
        "player_health": 100,
        "player_currency": 100,
        "rect":{
            "UI": {
                "cords": [735, 0 , 200, 540],
                "color": None,
                },
            "battlefield": {
                "cords": [0, 0 , 735, 540],
                "color": None,
                },
            "home": {
                "cords": [890, 0, 50, 50],
                "color": (0, 255, 255),
                },
            "pause": {
                "cords": [840, 0, 50, 50],
                "color": (0, 255, 0),
                },
            },
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [[Initialise["tower_testIMG"],"Linear tower", "penatrative!", True, 50], [Initialise["tower_testIMG"],"Parabolic tower", "knocks back!", True, 100], [Initialise["tower_testIMG"],"parabolic tower2", "knocks back!", True, 1000]]
        },

    # 2
    "level2": {}
}

Tower_preset = {
    "linear": {
        "dps": 10
    }
}