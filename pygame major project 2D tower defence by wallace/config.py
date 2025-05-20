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
    "enemy_ant_gIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_ant_gIMG.png').convert_alpha(), 1.3),
    "enemy_ant_sIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/enemy_ant_sIMG.png').convert_alpha(), 1.3),

    "attack_linearIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/attack_linearIMG.png').convert_alpha(), 0.7),
    "attack_parabolaIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/attack_parabolaIMG.png').convert_alpha(), 1),
    "tower_linearIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/tower_linearIMG.png').convert_alpha(), 0.8),
    "tower_parabolaIMG" : pygame.transform.scale_by(pygame.image.load('pygame major project 2D tower defence by wallace/assets/tower_parabolaIMG.png').convert_alpha(), 0.8),
    "queryIMG" : pygame.image.load('pygame major project 2D tower defence by wallace/assets/query.png').convert_alpha(),
    

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
    "home": { # button_data with rectangles of [85 + 285k, 70 + 235m, 200, 200 ]  -- > k and m are integers 
              # k represents the column number, m the row number
        # tutorial, level1, level2,/n level3, level4, level5
        "button_data": [[Initialise["queryIMG"],[85,70]],[Initialise["queryIMG"],[375,70]], [Initialise["queryIMG"],[655,70]], 
                        [Initialise["queryIMG"],[85,305]],[Initialise["queryIMG"],[375,305]], [Initialise["queryIMG"],[655,305]]],
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
                "image": Initialise["enemy_ant_gIMG"],
                "spawn_time": {1, 2,3,4,5}, # (tuple([x/100 for x in range(1000)])),
                "bounty": 15
            },
            "ant_s": {
                "health": 100,
                # distance in pixels
                "distance_per_second": 100,
                "image": Initialise["enemy_ant_sIMG"],
                "spawn_time": {7,8,9,20}, # (tuple([x/100 for x in range(1000)])),
                "bounty": 15
            }
        },
        "background_image": pygame.image.load('pygame major project 2D tower defence by wallace/assets/level1_background.png'),
        # (0,0) is not a valid checkpoint
        "checkpoints": [(0, 1), (260, 180), (120, 300), (300, 400), (530, 230), (710, 350), (570, 470), (700, 570)],
        "player_health": 100,
        "player_currency": 500,
        # pause, home
        "button_data": [[Initialise["queryIMG"],[840,0]],[Initialise["queryIMG"],[890,0]]],
        # UI, battlefield
        "rect_data":[[735, 0 , 200, 540],[0, 0 , 735, 540]],
        # for every shop item [tower_image, name: str, description: str, price: int, unlocked:bool, price:int]
        "shop_data": [["Linear tower", True], ["Parabola tower", True]]
        },

    # 2
    "level2": {}
}

Tower_preset = {
    "Linear tower": {
        "dps": 30,
        "description" : "penetrative!",
        "details" : ["This tower shoots a straight line nothing can stop, dealing damage to enemies on", "its path. This is also how linear graphs looks like - also a straight line, extending to", "infinity. The equation would be y = Ax or Ay = x"],
        "price": 50,
        "image" : Initialise["tower_linearIMG"],
        "range" : 200,
    },
    "Parabola tower": {
        "dps": 10,
        "description" : "Knocks back!",
        "details" : ["This tower shoots a growing curve knocking back enemies. This is also how parabola", " graphs looks like - also a curve curving at a linear rate. The equation would be y = Ax^2", " or Ay^2 = x, where ^2 means to the power of two. Be aware that you will only learn", " about parabolas facing verticly and horizontally in high school."],
        "price" : 100,
        "image" : Initialise["tower_parabolaIMG"],
        "range" : 230,
    }
}