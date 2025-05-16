# initialising
import pygame
import classes.enemy
import classes.tower
import classes.shop_item
from pygame.math import Vector2
import config
from datetime import datetime
import ingame_level_data

# start pygame
pygame.init()

# initialise icon and title
pygame.display.set_icon(pygame.image.load(config.Initialise["icon"]))
pygame.display.set_caption(config.Initialise["title"])

# get data from config file
screen = config.Initialise["screen"]
fps = config.Initialise["fps"]

# consider importing settings to a list that fit into pygame.font.SysFont() -> usually [text family: str, size: int, blod: bool, i]
player_health_font = pygame.font.SysFont(config.Initialise["player_health_font"][0], config.Initialise["player_health_font"][1], config.Initialise["player_health_font"][2], config.Initialise["player_health_font"][3])
player_currency_font = player_currency_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], config.Initialise["player_currency_font"][1], config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])
enemy_health_font = pygame.font.SysFont(config.Initialise["enemy_health_font"][0], config.Initialise["enemy_health_font"][1], config.Initialise["enemy_health_font"][2], config.Initialise["enemy_health_font"][3])



# getting data from classes
Enemy = classes.enemy.Enemy
Snake = classes.enemy.Snake
Linear = classes.tower.Linear
Parabola = classes.tower.Parabola
Ant_g = classes.enemy.Ant_g
Ant_s = classes.enemy.Ant_s
Shop_item = classes.shop_item.Shop_item


def generate_enemies(level : str):
    """
    prepare Enemy objects to be spawned

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    Result:
        Enemy objects to be spawned in the level is all in Enemy_prep_list which is stored in ingame_level_data.py,
        sorted according to their spawn time.
    """
    ingame_level_data.Ingame_data["Enemy_prep_list"] = []
    for enemy_type in config.Level_preset[level]["enemy_data"]:
        if enemy_type == "snake":
            for spawn_time in config.Level_preset[level]["enemy_data"]["snake"]["spawn_time"]:
                a = Snake(level, spawn_time)
                ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
        if enemy_type == "ant_g":
            for spawn_time in config.Level_preset[level]["enemy_data"]["ant_g"]["spawn_time"]:
                a = Ant_g(level, spawn_time)
                ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
        if enemy_type == "ant_s":
            for spawn_time in config.Level_preset[level]["enemy_data"]["ant_s"]["spawn_time"]:
                a = Ant_s(level, spawn_time)
                ingame_level_data.Ingame_data["Enemy_prep_list"].append(a)
    ingame_level_data.Ingame_data["Enemy_prep_list"].sort(key=find_spawn_time)

def generate_shop(level : str):
    """
    prepares Shop_item objects

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    Results:
        Shop_item objects to be shown in the level is all in Shop_item_list which is stored in ingame_level_data.py,
    """
    for i in range(0, len(config.Level_preset[level]["shop_data"])):
        a = Shop_item(i, level)
        a.resize(ingame_level_data.Ingame_data["resize_factor"])
        ingame_level_data.Ingame_data["Shop_item_list"].append(a)

def find_spawn_time(enemy):
    """
    find how many seconds after the level starts should the enemy spawn.
    Used in generate_enemies function.

    Args:
        enemy: A Enemy class object

    Returns:
        enemy.spawn_time: Spawn time of enemies
    """
# to be used in the function generate_enemies
    return(enemy.spawn_time)

def display_player_data():
    """
    draws player health and currency on the screen 
    
    Args:
        None
    
    Result:
        The data is being drawn on screen with suitable fonts
    """
    # health
    show_health = player_health_font.render(f"{round(ingame_level_data.Ingame_data["current_player_health"])}", True, (255, 255, 255))
    # draw it at left bottom corner with a 10px padding
    original_show_health_cords = (760, 5)
    screen.blit(show_health, [i * ingame_level_data.Ingame_data["resize_factor"] for i in original_show_health_cords])

    # currency
    show_currency = player_currency_font.render(f"{(ingame_level_data.Ingame_data["current_player_currency"])}", True, (255, 255, 0))

    original_show_currency_cords = (760, 25)
    screen.blit(show_currency, [i * ingame_level_data.Ingame_data["resize_factor"] for i in original_show_currency_cords])

def path_point_distance_check(level: str, location: Vector2, min_distance: float):
    """
    Check distance between the enemy path and a point, so that the towers will not be placed on the path

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer
        location: where to place
        min_distance: how far should the tower should be from any path
    
    Returns:
        distance: float
    """
    checkpoint_list = list(config.Level_preset[level]["checkpoints"])
    old_point = None
    min_distance *= ingame_level_data.Ingame_data["resize_factor"]

    for i in checkpoint_list:
        i = Vector2(i)

        if old_point:
            # some vector manipulations to find out distance of the 
            path_normalized = pygame.Vector2.normalize(i - old_point)
            projection_from_i = pygame.Vector2.dot(path_normalized, i - location) * path_normalized
            projection_from_old_point = pygame.Vector2.dot(path_normalized, old_point - location) * path_normalized
            
            """
             The dot product of two vectors that are parallel but in opposite directions is negative
             prevents checking for locations beyond the path segment           
            """

            if pygame.Vector2.dot(projection_from_i, projection_from_old_point) < 0:
                location_to_vector = projection_from_i - i + location
                magnitude = pygame.Vector2.magnitude(location_to_vector)
                
                if magnitude < min_distance:
                    return False
                
        # a circle near each check point to make up for a gap
        if pygame.Vector2.magnitude(i - location) < min_distance:
            return False

        # set up i as old_point to be used by next i
        old_point = i
        #print(old_point)
        #print("")
    
    # if did not return False
    return True

def revert_resizing_cords(cords):
    """
    revert the resizing process
    by getting a resized coordinate and divide components by resize_factor

    Args:
        cords: Vector2
    
    Return:
        original_cords: the original coordinate ( original when resize factor = 1 ) 
    """
    original_cords = Vector2(cords[0] / ingame_level_data.Ingame_data["resize_factor"], cords[1] / ingame_level_data.Ingame_data["resize_factor"])
    return original_cords


def place_tower(tower_type, level, location: Vector2):
    """
    Place a tower

    Args:
        tower_type: "Linear" or "Parabola"
        level: A string (levelx) representing the level to get the data from, where x is an integer
        location: where to place
    
    Result:
        A tower object from the Tower class is created and added into the Tower_list
    """
    original_location = revert_resizing_cords(location)
    # place tower base at where clicked
    original_location = [original_location[0], original_location[1] - 35]

    if path_point_distance_check(level, location, 60*ingame_level_data.Ingame_data["resize_factor"]):
        match tower_type:
            case "Linear":
                tower = Linear(tower_type, level, original_location)
                ingame_level_data.Ingame_data["Tower_list"].add(tower)
            case "Parabola":
                tower = Parabola(tower_type, level, original_location)
                ingame_level_data.Ingame_data["Tower_list"].add(tower)

        tower.resize(ingame_level_data.Ingame_data["resize_factor"])
        ingame_level_data.Ingame_data["tower_placed"] += 1
        ingame_level_data.Ingame_data["held_item"] = None

    else:
        error_list.append([2, "Too close to path."])

def spawn_enemies():
    """
    Spawn prepared enemies

    Args:
        None
    
    Result:
        A enemy object from the Tower class is moved from the Enemy_prep_list to the ENemy_list
    """
    current_time = pygame.time.get_ticks() / 1000 - time_level_init
    while 0 < len(Enemy_prep_list) and Enemy_prep_list[0].spawn_time <= current_time:
        Enemy_prep_list[0].resize(ingame_level_data.Ingame_data["resize_factor"])
        Enemy_list.add(Enemy_prep_list[0])
        Enemy_prep_list.pop(0)

def resize_factor_get():
    """
    find the factor for everything to be resized to

    Args:
        None
    
    Result:
        resize_factor is calculated in order to keep everything in the screen despite the size change 
    """
    old_width, old_height = config.Initialise["screen_size"]
    new_width, new_height = pygame.display.get_surface().get_size()
    
    # compare whether old or new
    width_factor = new_width / old_width
    height_factor = new_height / old_height

    if width_factor <= height_factor:
        ingame_level_data.Ingame_data["resize_factor"] = width_factor
    else:
        ingame_level_data.Ingame_data["resize_factor"] = height_factor

def import_rect_settings(level : str):
    """
    resize rectangles

    Args:
        level: A string (levelx) representing the level to get the data from, where x is an integer

    
    Result:
        rectangles representing buttons are resized
    """
# with the format of "level1" for the level parameter

    # import the new rectangle settings into ingame data by first clearing the old one
    ingame_level_data.Ingame_data["rect"] = {}
    for i in config.Level_preset[level]["rect"]:
        rect = { # create a copy of the dictionary
            "cords": list(config.Level_preset[level]["rect"][str(i)]["cords"]),  
            "color": config.Level_preset[level]["rect"][str(i)]["color"]  
        }
        ingame_level_data.Ingame_data["rect"].update({i : rect})

        for j in range(0,4): # make change due to the resizing
                    ingame_level_data.Ingame_data["rect"][str(i)]["cords"][j] *= ingame_level_data.Ingame_data["resize_factor"]

def error_message():
    """
    draws a alerting message on the screen 
    
    Args:
        None
    
    Result:
        The message is being drawn on screen with suitable fonts
    """
    for i in error_list:
        if i[0] > 0:
            show_error = player_currency_font.render(i[1], True, (255, 0, 0))
            screen.blit(show_error, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [300, 500 - 40 * error_list.index(i)]])
            i[0] -= 1 / fps
        else:
            error_list.remove(i)




# Game loop
running = True

# where level 0 is the homepage and level 1 will be battle places.
level_selected = 0

# stores in format of a list containing duration in seconds and text
# eg. [1, "Don't press that"] 
error_list = []

# initialise time right before the loop begins to avoid the delay from running other codes
clock = pygame.time.Clock()


while running:
    match level_selected:
        case 0:
            
            home_running = True

            # set the buttons
            import_rect_settings("home")
            tutorial_button_rect = ingame_level_data.Ingame_data["rect"]["tutorial"]["cords"]
            level1_button_rect = ingame_level_data.Ingame_data["rect"]["level1"]["cords"]
            player_currency_font = player_currency_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], round(config.Initialise["player_currency_font"][1]  * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])
            player_health_font = pygame.font.SysFont(config.Initialise["player_health_font"][0], round(config.Initialise["player_health_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_health_font"][2], config.Initialise["player_health_font"][3])


            while home_running:
                screen.fill((232, 185, 77))

                # display buttons, temporary
                for i in ingame_level_data.Ingame_data["rect"]:
                    level_button_cords = ingame_level_data.Ingame_data["rect"][str(i)]["cords"]
                    pygame.draw.rect(screen, ingame_level_data.Ingame_data["rect"][str(i)]["color"], [i for i in level_button_cords])
                
                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # quit the loop of this level and game level
                        running = False
                        home_running = False

                    # Buttons
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if tutorial_button_rect[0] <= mouse[0] <= (tutorial_button_rect[0] + tutorial_button_rect[2]) and tutorial_button_rect[1] <= mouse[1] <= (tutorial_button_rect[1] + tutorial_button_rect[3]):
                            # quit the loop of this level and start that of level 1
                            error_list.append([2, "Not yet implemented."])
                        if level1_button_rect[0] <= mouse[0] <= (level1_button_rect[0] + level1_button_rect[2]) and level1_button_rect[1] <= mouse[1] <= (level1_button_rect[1] + level1_button_rect[3]):
                            # quit the loop of this level and start that of level 1
                            level_selected = 1
                            home_running = False

                    elif event.type == pygame.VIDEORESIZE:
                        resize_factor_get()
                        import_rect_settings("home")
                        tutorial_button_rect = ingame_level_data.Ingame_data["rect"]["tutorial"]["cords"]
                        level1_button_rect = ingame_level_data.Ingame_data["rect"]["level1"]["cords"]
                        player_currency_font = player_currency_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], round(config.Initialise["player_currency_font"][1]  * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])
                        player_health_font = pygame.font.SysFont(config.Initialise["player_health_font"][0], round(config.Initialise["player_health_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_health_font"][2], config.Initialise["player_health_font"][3])


                error_message()

                pygame.display.update()
                clock.tick(fps)

        case 1:
            level1_running = True
            # Initialise level 1
            ingame_level_data.Ingame_data["current_player_health"] = config.Level_preset["level1"]["player_health"]
            ingame_level_data.Ingame_data["current_player_currency"] = config.Level_preset["level1"]["player_currency"]
            generate_enemies("level1")
            generate_shop("level1")
            background = config.Level_preset["level1"]["background_image"]
            a = 0

            # import retangles
            import_rect_settings("level1")
            home_button_rect = ingame_level_data.Ingame_data["rect"]["home"]["cords"]
            pause_button_rect = ingame_level_data.Ingame_data["rect"]["pause"]["cords"]
            UI_rect = ingame_level_data.Ingame_data["rect"]["UI"]["cords"]
            battlefield_rect = ingame_level_data.Ingame_data["rect"]["battlefield"]["cords"]
            background = pygame.transform.scale_by(config.Level_preset["level1"]["background_image"], ingame_level_data.Ingame_data["resize_factor"])

            # The enemies spawn relative to when the
            time_level_init = pygame.time.get_ticks()/1000

            # get list from the file once and for all for this 
            Enemy_list = ingame_level_data.Ingame_data["Enemy_list"]
            Tower_list = ingame_level_data.Ingame_data["Tower_list"]
            Enemy_prep_list = ingame_level_data.Ingame_data["Enemy_prep_list"]
            Attack_list = ingame_level_data.Ingame_data["Attack_list"]
            Shop_item_list = ingame_level_data.Ingame_data["Shop_item_list"]

            ingame_level_data.Ingame_data["held_item"] = None

            # start loop for level 1
            while level1_running:
                # for the actual time passed
                start_time = datetime.now()


                # insert background image
                screen.fill((30, 10, 0))
                screen.blit(background, (0, 0))

                # display player health
                display_player_data()
                
                error_message()

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
                Enemy_list.draw(screen)

                for enemy in Enemy_list:
                    enemy.show_health(enemy.health, enemy.location)
                    

                for shop_item in Shop_item_list:
                    shop_item.draw()

                # display buttons, temporary
                for i in ingame_level_data.Ingame_data["rect"]:
                    button_cords = ingame_level_data.Ingame_data["rect"][str(i)]["cords"]
                    if ingame_level_data.Ingame_data["rect"][str(i)]["color"]:
                        pygame.draw.rect(screen, ingame_level_data.Ingame_data["rect"][str(i)]["color"], [i for i in button_cords])
                

                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        level1_running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        # print(mouse) # for testing
                        # UI
                        if UI_rect[0] <= mouse[0] <= (UI_rect[0] + UI_rect[2]) and UI_rect[1] <= mouse[1] <= (UI_rect[1] + UI_rect[3]):
                                # pressed functional buctions
                            if home_button_rect[0] <= mouse[0] <= (home_button_rect[0] + home_button_rect[2]) and home_button_rect[1] <= mouse[1] <= (home_button_rect[1] + home_button_rect[3]):
                                level_selected = 0
                                level1_running = False
                                ingame_level_data.Ingame_data["Enemy_dead_list"].empty()
                                ingame_level_data.Ingame_data["Enemy_list"].empty()
                                ingame_level_data.Ingame_data["Enemy_prep_list"] = []
                                ingame_level_data.Ingame_data["Tower_list"].empty()

                            elif pause_button_rect[0] <= mouse[0] <= (pause_button_rect[0] + pause_button_rect[2]) and pause_button_rect[1] <= mouse[1] <= (pause_button_rect[1] + pause_button_rect[3]):
                                pause = True
                                message = player_health_font.render("click again to resume." , True, (255, 255, 255))
                                message_rect = message.get_rect()
                                message_rect.center = (config.Initialise["screen_size"][0] / 2, config.Initialise["screen_size"][1] / 2)
                                screen.blit(message, message_rect)
                                pygame.display.update()
                                while pause:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            pause = False

                            elif ingame_level_data.Ingame_data["held_item"] == None: # pressed shop and has not bought anything yet
                                for i in Shop_item_list:
                                    if i.check_press(mouse): # 0 for nothing, 1 for Linear_tower, 2 for Parabola_tower  
                                        if i.name == "Linear tower":
                                            if ingame_level_data.Ingame_data["current_player_currency"] >= i.price: # enough currency to buy!
                                                ingame_level_data.Ingame_data["current_player_currency"] -= i.price
                                                ingame_level_data.Ingame_data["held_item"] = 1
                                                break
                                            else: error_list.append([2, f"You need {i.price - ingame_level_data.Ingame_data["current_player_currency"]} more to buy the tower."])

                                        elif i.name == "Parabola tower":
                                            if ingame_level_data.Ingame_data["current_player_currency"] >= i.price: # enough currency to buy!
                                                ingame_level_data.Ingame_data["current_player_currency"] -= i.price
                                                ingame_level_data.Ingame_data["held_item"] = 2
                                                break
                                            else: error_list.append([2, f"You need {i.price - ingame_level_data.Ingame_data["current_player_currency"]} more to buy the tower."])
                                            
                                        else:
                                           error_list.append([2, i.name + 'this is not yet implemented'])

                            else: # clicked on shop UI with a item held -> they should not
                                error_list.append([2, "You are holding a tower! click on the battlefield to place it."]) 

                        #  pressing on the field
                        elif battlefield_rect[0] <= mouse[0] <= (battlefield_rect[0] +battlefield_rect[2]) and battlefield_rect[1] <= mouse[1] <= (battlefield_rect[1] +battlefield_rect[3]): 
                            match ingame_level_data.Ingame_data["held_item"]:
                                case None: # check if pressing on tower
                                    clicked = False
                                    for i in Tower_list:
                                        if i.check_press(mouse):
                                            clicked = True
                                            break
                                    if not clicked: # not pressing on any tower
                                        error_list.append([2, "You are not holding or clicking on a tower."])

                                case 1:
                                    place_tower("Linear", "level1", Vector2(pygame.mouse.get_pos()))

                                case 2:
                                    place_tower("Parabola", "level1", Vector2(pygame.mouse.get_pos()))
                        
                        else: # clicking out of bounds
                            error_list.append([2, "Here is out of bounds!"])


                    elif event.type == pygame.VIDEORESIZE:
                        resize_factor_get()
                        import_rect_settings("level1")
                        
                        home_button_rect = ingame_level_data.Ingame_data["rect"]["home"]["cords"]
                        pause_button_rect = ingame_level_data.Ingame_data["rect"]["pause"]["cords"]
                        UI_rect = ingame_level_data.Ingame_data["rect"]["UI"]["cords"]
                        battlefield_rect = ingame_level_data.Ingame_data["rect"]["battlefield"]["cords"]
                        player_health_font = pygame.font.SysFont(config.Initialise["player_health_font"][0], round(config.Initialise["player_health_font"][1] * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_health_font"][2], config.Initialise["player_health_font"][3])
                        player_currency_font = player_currency_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], round(config.Initialise["player_currency_font"][1]  * ingame_level_data.Ingame_data["resize_factor"]), config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])

                        for i in Enemy_list:
                            i.resize(ingame_level_data.Ingame_data["resize_factor"])
                        for j in Tower_list:
                            j.resize(ingame_level_data.Ingame_data["resize_factor"])
                        for k in Attack_list:
                            k.resize(ingame_level_data.Ingame_data["resize_factor"])
                        for l in Shop_item_list:
                            l.resize(ingame_level_data.Ingame_data["resize_factor"])

                        background = pygame.transform.scale_by(config.Level_preset["level1"]["background_image"], ingame_level_data.Ingame_data["resize_factor"])


                # move enemies from prep list to list at certain time
                spawn_enemies()
                        # OLD:
                        #        time = pygame.time.get_ticks()/1000 - time_level_init
                        #        for enemy in Enemy_prep_list:
                        #            if time >= enemy.spawn_time:
                        #                Enemy_prep_list.remove(enemy)
                        #                Enemy_list.add(enemy)


                # check if the player have any health left --> should add a death message / screen / score
                if ingame_level_data.Ingame_data["current_player_health"] <= 0:
                    running = False
                    level1_running = False

                # put the changed things on screen
                pygame.display.update()

                # print(datetime.now() - start_time, "tower placed:", a)
                clock.tick(fps)

pygame.quit()
