import pygame
from pygame import Vector2
import config
import ingame_level_data
import classes.attack
import copy
import math

# get data from config file
screen = config.Initialise["screen"]
towerIMG = config.Initialise["towerIMG"]
fps = config.Initialise["fps"]
player_health_font = pygame.font.SysFont(config.Initialise["player_health_font"][0], config.Initialise["player_health_font"][1], config.Initialise["player_health_font"][2], config.Initialise["player_health_font"][3])

# get attacks from attack
Linear_attack = classes.attack.Linear_attack
Parabola_attack = classes.attack.Parabola_attack


class Tower(pygame.sprite.Sprite):
    #  these init values will be obtained from the config file
    def __init__(self, tower_type, level, location: Vector2):
        pygame.sprite.Sprite.__init__(self)
        self.tower_type = tower_type
        # in format of "levelx"
        self.level = level
        self.original_location = Vector2(location)
        self.location = Vector2(location)
        self.resize_factor = 1

        self.range = None
        # stores an object of class enemy
        self.targeted_enemy = None
        self.facing_vector = None
        self.distance_between_target_and_tower = None

        self.image = towerIMG
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.cooldown = 0

    def aim(self):
        # get list from the file once and for all for this aim
        Enemy_list = ingame_level_data.Ingame_data["Enemy_list"]

        # ending this function if there is no enemies at all
        if not Enemy_list:
            self.targeted_enemy = None
            return

        else:
            # If tower is not aiming at anyone, and there is enemies
            if not self.targeted_enemy:
                # for each enemy in Enemy_list, if it is in range, add it to the list
                enemies_in_range = [enemy for enemy in Enemy_list if (self.location - enemy.location).length() <= self.range]
                if enemies_in_range:
                    # "Find the enemy in enemies_in_range whose distance from this tower is smallest
                    self.targeted_enemy = min(enemies_in_range, key=lambda e: (self.location - e.location).length())

            else:
                target_location = copy.deepcopy(self.targeted_enemy.location)
                if self.targeted_enemy in Enemy_list and (self.location - target_location).length() <= self.range:
                    # enemy is still aimable
                    # draw an aiming lense like shape
       #             pygame.draw.circle(screen, (255, 255, 255), target_location, 10, width=4)
        #            pygame.draw.line(screen, (255, 255, 255), (target_location.x - 15, target_location.y), (target_location.x - 10, target_location.y), 4)
         #           pygame.draw.line(screen, (255, 255, 255), (target_location.x + 15, target_location.y), (target_location.x + 10, target_location.y), 4)
          #          pygame.draw.line(screen, (255, 255, 255), (target_location.x, target_location.y + 15), (target_location.x, target_location.y + 10), 4)
           #         pygame.draw.line(screen, (255, 255, 255), (target_location.x, target_location.y - 15), (target_location.x, target_location.y - 10), 4)
                    self.facing_vector = self.location - target_location
                    self.shoot()

                else:
                    self.targeted_enemy = None

    def shoot(self):
        pass

    def resize(self, resize_factor: float):
        self.image = pygame.transform.scale_by(towerIMG, resize_factor)
        self.location = (self.original_location[0] * resize_factor , self.original_location[1] * resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.resize_factor = resize_factor

    def check_press(self, mouse_pos: Vector2):
        # check if pressed on this item
        # self.location is the center of towers
        self.x = self.location[0]
        self.y = self.location[1]
        if (self.x - self.rect[2] / 2) <= mouse_pos[0] <= (self.x + self.rect[2] / 2) and (self.y - self.rect[3] / 2) <= mouse_pos[1] <= (self.y + self.rect[3] / 2):
            # clicked on this tower
            return True
        else: return False

class Linear(Tower):
    def __init__(self, tower_type, level, location: Vector2):
        super().__init__(tower_type, level, location)
        self.range = config.Tower_preset["Linear tower"]["range"]

    def shoot(self):
        ingame_level_data.Ingame_data["Attack_list"].add(Linear_attack(self.resize_factor, self.facing_vector, self.location))


class Parabola(Tower):
    def __init__(self, tower_type, level, location: list):
        super().__init__(tower_type, level, location)
        self.range = config.Tower_preset["Parabola tower"]["range"]
        self.extension_calculation = 0 
        self.extension_value = 0   # will be rotated between - to 1 using a sine function
        self.attack_image_facing = pygame.math.Vector2(-1, 0)
      
        self.facing_vector = pygame.math.Vector2(100, -10) # testing, will implement method to change the facing
        self.angle = self.facing_vector.angle_to(self.attack_image_facing)

    def aim(self): # aim is called every tick
        # attacks like a parabola extending then disappear

        if self.cooldown <= 0: # no in cooldown --> may attack
            if self.extension_calculation < math.pi / 2: # not yet max
                self.extension_calculation += math.pi / fps / 4 # takes 2 second to get to full
                self.extension_value = math.sin(self.extension_calculation) * 5
        #         if self.extension_value < 0:
        #            self.extension_value = -self.extension_value

            else: # reached the max, enter cooldown
                self.extension_calculation = 0
                self.cooldown = 2 * fps # waits 2 seconds before firing again
            
            self.shoot()
            
        else: # in cooldown --> may not attack
            self.cooldown -= 1

    def rotate(self, facing_location): # change facing vector, thus change angle
        self.facing_vector = self.location - pygame.math.Vector2(facing_location)
        self.angle = self.facing_vector.angle_to(self.attack_image_facing)

    def shoot(self):
        ingame_level_data.Ingame_data["Attack_list"].add(Parabola_attack(self.resize_factor, self.angle, self.location, self.extension_value))

    def check_press(self, mouse_pos: Vector2):
        # check if pressed on this item
        # self.location is the center of towers 
        self.x = self.location[0]
        self.y = self.location[1]
        if (self.x - self.rect[2] / 2) <= mouse_pos[0] <= (self.x + self.rect[2] / 2) and (self.y - self.rect[3] / 2) <= mouse_pos[1] <= (self.y + self.rect[3] / 2):
            pygame.draw.rect(screen, (0, 0, 0), [i * ingame_level_data.Ingame_data["resize_factor"] for i in [735, 50, 205, 540]])
            # instructions
            click_message1 = player_health_font.render("Click on the direction ", True, (255, 255, 255))
            click_message2 = player_health_font.render("the tower should face! ", True, (255, 255, 255))
            screen.blit(click_message1, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [735, 50]])
            screen.blit(click_message2, [i * ingame_level_data.Ingame_data["resize_factor"] for i in [735, 75]])
            pygame.display.update([i * ingame_level_data.Ingame_data["resize_factor"] for i in [735, 50, 205, 540]])
            
            # clicked on this tower
            menu = True
            while menu:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        menu = False
                        break
            self.rotate(mouse)
            return True
        else: return False
