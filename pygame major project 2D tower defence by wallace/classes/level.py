class levelselector:
    def __init__(self):
        self.type = " "

    # create a string representation of the object for debugging
    def __repr__(self):
        return "this is a empty level selector!"
    
    def run(self):
        print(self.__repr__)


class initialise(levelselector):
    def __init(self):
        super.__init__()

    def run(self):
        # importing
        import pygame
        import classes.enemy
        import classes.tower
        from pygame.math import Vector2
        import config
        from datetime import datetime
        import ingame_level_data

        # start pygame
        pygame.init()

        # initialise icon and title
        pygame.display.set_icon(pygame.image.load('pygame major project 2D tower defence by wallace/assets/game-icon.png'))
        pygame.display.set_caption("Maths defence")

        # get data from config file
        screen = config.screen
        fps = config.fps
        player_health_font = config.player_health_font
        player_currency_font = config.player_currency_font


        # getting data from classes
        Enemy = classes.enemy.Enemy
        Snake = classes.enemy.Snake
        linear = classes.tower.linear
        Ant_g = classes.enemy.Ant_g

        # with the format of "level1" for the level parameter
        def generate_enemies(level):
            for enemy_type in config.Level_preset[level]["enemy_data"]:
                if enemy_type == "snake":
                    for spawn_time in config.Level_preset[level]["enemy_data"]["snake"]["spawn_time"]:
                        a = Snake(level, spawn_time)
                        ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
                if enemy_type == "ant_g":
                    for spawn_time in config.Level_preset[level]["enemy_data"]["ant_g"]["spawn_time"]:
                        a = Ant_g(level, spawn_time)
                        ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
            ingame_level_data.Ingame_data["Enemy_prep_list"].sort(key=find_spawn_time)

        
        # to be used in the function generate_enemies
        def find_spawn_time(e):
            return(e.spawn_time)


        def display_player_data():
            # health
            show_health = player_health_font.render(f"{round(ingame_level_data.Ingame_data["current_player_health"])}", True, (255, 255, 255))
            # draw it at left bottom corner with a 10px padding
            screen.blit(show_health, (760, 5))

            # currency
            show_currency = player_currency_font.render(f"{(ingame_level_data.Ingame_data["current_player_currency"])}", True, (255, 255, 0))
            screen.blit(show_currency, (760, 25))


        def place_tower(tower_type, level, location: Vector2):
            if tower_type == "linear":
                ingame_level_data.Ingame_data["Tower_list"].add(linear(tower_type, level, location))

        def spawn_enemies():
            current_time = pygame.time.get_ticks() / 1000 - time_level_init
            while 0 < len(Enemy_prep_list) and Enemy_prep_list[0].spawn_time <= current_time:
                Enemy_list.add(Enemy_prep_list[0])
                Enemy_prep_list.pop(0)

        # Game loop
        running = True

        # initialise time right before the loop begins to avoid the delay from running other codes
        clock = pygame.time.Clock()

        # where level 0 is the homepage and level 1 will be battle places.
        level_selected = 0