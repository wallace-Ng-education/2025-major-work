import pygame
from pygame import Vector2
import config
import ingame_level_data
import classes.attack
import copy

# get data from config file
screen = config.Initialise["screen"]
tower_testIMG = config.Initialise["tower_testIMG"]
bullet_IMG = config.Initialise["bullet_IMG"]

# get attacks from attack
linear_attack = classes.attack.linear_attack


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

        self.image = tower_testIMG
        self.rect = self.image.get_rect()
        self.rect.center = self.location

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
        self.image = pygame.transform.scale_by(tower_testIMG, resize_factor)
        self.location = (self.original_location[0] * resize_factor , self.original_location[1] * resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.resize_factor = resize_factor


class linear(Tower):
    def __init__(self, tower_type, level, location: Vector2):
        super().__init__(tower_type, level, location)
        self.range = 350

    def shoot(self):
        ingame_level_data.Ingame_data["Attack_list"].add(linear_attack(self.resize_factor, self.facing_vector, self.location))
