import pygame
import config
from pygame.math import Vector2
import ingame_level_data
import random

# get global data from config
screen = config.screen
fps = config.fps
enemy_health_font = config.enemy_health_font
player_health = config.Level_preset["level1"]["player_health"]


# use the defined sprite class for its functions
class Enemy(pygame.sprite.Sprite):
    #  these init values will be obtained from the config file
    def __init__(self, enemy_type, level, spawn_time):
        pygame.sprite.Sprite.__init__(self)

        # get defined data from input
        ##################################################################################
        self.enemy_type = enemy_type
        # in format of "levelx"
        self.level = level
        self.spawn_time = spawn_time

        # get the data according to the enemy type
        ##################################################################################
        # distance/frame = (distance/second) / (frame/second)
        # so the speed of enemies will not change when changing the fps
        self.distance_per_frame = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["distance_per_second"] / fps
        self.health = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["health"]
        self.checkpoints = config.Level_preset[self.level]["checkpoints"]
        self.image = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["image"]
        self.bounty = config.Level_preset[self.level]["enemy_data"][self.enemy_type]["bounty"]

        # get common data for all enemies
        ##################################################################################
        # initially starts as first checkpoint, i.e. first checkpoint is spawn point
        self.location = Vector2(self.checkpoints[0])
        # initially goes towards the 2nd checkpoint in the list of checkpoints
        self.target_checkpoint = 1

#        self.image = config.Level_data[self.level]["enemy_data"][self.enemy_type]["image"]
        self.movement = None
        self.target_location = None

        self.rect = self.image.get_rect()
        self.rect.center = self.location

        self.enemy_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.enemy_mask.to_surface()

    # show health of enemy, logically belongs to the enemy class
    def show_health(self, health: int, location: Vector2):
        show_health = enemy_health_font.render(f"{round(health)}", True, (255, 255, 0))
        screen.blit(show_health, location)


    def death(self):
        ingame_level_data.Ingame_data["current_player_currency"] += self.bounty
        self.kill()


    def move(self):
        # modification of global variable needed
        global player_health
        # check if there is still checkpoints to go
        if self.target_checkpoint < len(self.checkpoints):
            # O is origin, T is the target checkpoint. This is the vector OT
            self.target_location = Vector2(self.checkpoints[self.target_checkpoint])

            # self.location is OL the vector from origin to the current checkpoint.
            # Therefore, self.movement is OT - OL = LO + OT = LT,
            # which is the vector for moving from current checkpoint to the targeted checkpoint.
            self.movement = self.target_location - self.location

            distance_from_target = self.movement.length()
            # if the enemy is very close to the previous one
            if distance_from_target < self.distance_per_frame:
                # move for the remaining distance_from_target between it and the target
                self.location += self.movement.normalize()*distance_from_target
                # change target
                self.target_checkpoint += 1
            else:  # haven't reached
                # normalise converts the vector to a vector with total length of 1
                # therefore the enemy will move in the movement's direction for a number(as defined in speed) of pixels
                self.location += self.movement.normalize()*self.distance_per_frame

            self.rect.center = self.location
            self.show_health(self.health, self.location)
        # enemy has finished path
        else:
            ingame_level_data.Ingame_data["current_player_health"] -= self.health
            self.death()
#            print('-' , self.health)  #  show health when finish path


class Snake(Enemy):
    # equal sign
    def __init__(self, level, spawn_time):
        Enemy.__init__(self, "snake", level, spawn_time)


class Ant_g(Enemy):
    # greater than
    def __init__(self, level, spawn_time):
        Enemy.__init__(self, "ant_g", level, spawn_time)
        self.randint: int = random.randint(-100,100)

        # get the width needed to center this message, allow functions in this class to accesss the width 
        health_message_align: str = f"{self.randint} "
        health_message_align = enemy_health_font.render(health_message_align, True, (255, 255, 0))
        # +9 in consideration of the length of the "<" symbol
        self.message_width_half: float = health_message_align.get_rect()[2] + 9

    # show a health and the number that it needs to be greater than
    def show_health(self, health: int, location: Vector2):
        # get the strings
        health_message: str = f"{self.randint} < {round(health + self.randint)}"
        # turn the strings into pygame rectangles
        health_message = enemy_health_font.render(health_message, True, (255, 255, 0))

        # center the ">" in health_message 
        message_height_half = health_message.get_rect()[3] / 2
        screen.blit(health_message, (location[0] - self.message_width_half, location[1] - message_height_half))


class Ant_s(Enemy):
    # smaller than
    def __init__(self, level, spawn_time):
        Enemy.__init__(self, "ant_s", level, spawn_time)
        self.randint: int = random.randint(-100,100)
        self.appearent_health: int = self.randint - self.health 

        # get the width needed to center this message, allow functions in this class to accesss the width 
        health_message_align: str = f"{self.randint} "
        health_message_align = enemy_health_font.render(health_message_align, True, (255, 255, 0))
        # +9 in consideration of the length of the ">" symbol
        self.message_width_half: float = health_message_align.get_rect()[2] + 9

    # show a health and the number that it needs to be greater than
    def show_health(self, health: int, location: Vector2):
        # get the strings
        health_message: str = f"{self.randint} > {round(health + self.randint)}"
        # turn the strings into pygame rectangles
        health_message = enemy_health_font.render(health_message, True, (255, 255, 0))

        # center the ">" in health_message 
        message_height_half = health_message.get_rect()[3] / 2
        screen.blit(health_message, (location[0] - self.message_width_half, location[1] - message_height_half))

##########################################################################