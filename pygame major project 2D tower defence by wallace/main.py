# initialising
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
pygame.display.set_icon(pygame.image.load('assets/game-icon.png'))
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


# with the format of "level1" for the level parameter
def generate_enemies(level):
    for spawn_time in config.Level_preset[level]["enemy_data"]["snake"]["spawn_time"]:
        a = Snake(level, spawn_time)
        ingame_level_data.Ingame_data["Enemy_prep_list"].add(a)


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


# Game loop
running = True

# initialise time right before the loop begins to avoid the delay from running other codes
clock = pygame.time.Clock()

# where level 0 is the homepage and level 1 will be battle places.
level_selected = 0

while running:
    match level_selected:
        case 0:
            home_running = True
            while home_running:
                screen.fill((232, 185, 77))
    
                pygame.draw.rect(screen, (0, 200, 0), [100, 100, 50, 50])
    
                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit the loop of this level and game level
                        running = False
                        home_running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # testing mouse
                        mouse = pygame.mouse.get_pos()
                        if 100 <= mouse[0] <= 150 and 100 <= mouse[1] <= 150:
                            # quit the loop of this level and start that of level 1
                            level_selected = 1
                            home_running = False
    
                pygame.display.update()
                clock.tick(fps)

        case 1:
            level1_running = True
            # Initialise level 1
            ingame_level_data.Ingame_data["current_player_health"] = config.Level_preset["level1"]["player_health"]
            ingame_level_data.Ingame_data["current_player_currency"] = config.Level_preset["level1"]["player_currency"]
            generate_enemies("level1")
            background = config.Level_preset["level1"]["background_image"]
            tower_placed = 0

            # The enemies spawn relative to when the
            time_level_init = pygame.time.get_ticks()/1000

            # start loop for level 1
            while level1_running:
                # test for the actual time taken per frame
                # start_time = datetime.now()

                # get list from the file once and for all for this aim
                Enemy_list = ingame_level_data.Ingame_data["Enemy_list"]
                Tower_list = ingame_level_data.Ingame_data["Tower_list"]
                Enemy_prep_list = ingame_level_data.Ingame_data["Enemy_prep_list"]
                Attack_list = ingame_level_data.Ingame_data["Attack_list"]

                # insert background image
                screen.blit(background, (0, 0))

                # display player health
                display_player_data()

                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        level1_running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        # print(mouse)
                        place_tower("linear", "level1", Vector2(pygame.mouse.get_pos()))
                        tower_placed += 1

                        # home & reset button
                        if 890 <= mouse[0] <= 940 and 0 <= mouse[1] <= 50:
                            level_selected = 0
                            level1_running = False
                            ingame_level_data.Ingame_data["Enemy_dead_list"].empty()
                            ingame_level_data.Ingame_data["Enemy_list"].empty()
                            ingame_level_data.Ingame_data["Enemy_prep_list"].empty()
                            ingame_level_data.Ingame_data["Tower_list"].empty()

                Enemy_list.draw(screen)
                Tower_list.draw(screen)

                for tower in Tower_list:
                    tower.aim()
                #       tower.shoot()

                Attack_list.draw(screen)
                for attack in Attack_list:
                    attack.tick()

                # make every Enemy object do what they are supposed to
                for enemy in Enemy_list:
                    enemy.move()

                # move enemies from prep list to list at certain time
                time = pygame.time.get_ticks()/1000 - time_level_init
                for enemy in Enemy_prep_list:
                    if time >= enemy.spawn_time:
                        Enemy_prep_list.remove(enemy)
                        Enemy_list.add(enemy)

                # check if the player have any health left --> should add a death message / screen / score
                if ingame_level_data.Ingame_data["current_player_health"] <= 0:
                    running = False
                    level1_running = False

                pygame.draw.rect(screen, (0, 200, 0), [890, 0, 50, 50])

                # put the changed things on screen
                pygame.display.update()

                # print(datetime.now() - start_time, "tower placed:", tower_placed)
                clock.tick(fps)

pygame.quit()
