import pygame
from pygame import Vector2
import config
import ingame_level_data
import classes.attack

# get data from config file
screen = config.screen
tower_testIMG = config.tower_testIMG
bullet_IMG = config.bullet_IMG

# get attacks from attack
linear_attack = classes.attack.linear_attack


class Tower(pygame.sprite.Sprite):
    #  these init values will be obtained from the config file
    def __init__(self, tower_type, level, location: Vector2):
        pygame.sprite.Sprite.__init__(self)
        self.tower_type = tower_type
        # in format of "levelx"
        self.level = level
        self.location = location

        self.range = None
        # stores an object of class enemy
        self.targeted_enemy = None
        self.facing_vector = None
        self.distance_between_target_and_tower = None

        self.image = tower_testIMG
        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def aim(self):
        pygame.draw.circle(screen, (255, 255, 255), self.location, self.range, width=2)
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
                if self.targeted_enemy in Enemy_list and (self.location - self.targeted_enemy.location).length() <= self.range:
                    # enemy is still aimable
                    # draw an aiming lense like shape
                    pygame.draw.circle(screen, (255, 255, 255), self.targeted_enemy.location, 10, width=4)
                    pygame.draw.line(screen, (255, 255, 255), (self.targeted_enemy.location.x - 15, self.targeted_enemy.location.y), (self.targeted_enemy.location.x - 10, self.targeted_enemy.location.y), 4)
                    pygame.draw.line(screen, (255, 255, 255), (self.targeted_enemy.location.x + 15, self.targeted_enemy.location.y), (self.targeted_enemy.location.x + 10, self.targeted_enemy.location.y), 4)
                    pygame.draw.line(screen, (255, 255, 255), (self.targeted_enemy.location.x, self.targeted_enemy.location.y + 15), (self.targeted_enemy.location.x, self.targeted_enemy.location.y + 10), 4)
                    pygame.draw.line(screen, (255, 255, 255), (self.targeted_enemy.location.x, self.targeted_enemy.location.y - 15), (self.targeted_enemy.location.x, self.targeted_enemy.location.y - 10), 4)
                    self.facing_vector = self.location - self.targeted_enemy.location
                    self.shoot()

                else:
                    self.targeted_enemy = None

    def shoot(self):
        pass


class linear(Tower):
    def __init__(self, tower_type, level, location: Vector2):
        super().__init__(tower_type, level, location)
        self.range = 350

    def shoot(self):
        ingame_level_data.Ingame_data["Attack_list"].add(linear_attack(self.facing_vector, self.location))
