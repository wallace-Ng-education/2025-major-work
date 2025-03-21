import pygame
from pygame import Vector2
import ingame_level_data
import config

# get data from config file
screen = config.screen
bullet_IMG = config.bullet_IMG
fps = config.fps


class Attacks(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.hit_list = None
        self.hit_box = None

    def tick(self):
        pass


class linear_attack(Attacks):
    def __init__(self, direction: Vector2, location: Vector2):
        Attacks.__init__(self)

        self.location = location
        self.direction = direction

        # the direction this attack will go
        self.hit_list = None
        self.East = pygame.math.Vector2(1, 0)
        # clockwise angle from East axis
        self.angle = self.direction.angle_to(self.East)

        self.image = pygame.transform.rotate(bullet_IMG, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        # try line collision
        self.line_start = self.location + self.direction.normalize() * 1090
        self.line_end = self.location - self.direction.normalize() * 1090

        # creating a mask for pixel perfect collision check
        self.linear_mask = pygame.mask.from_surface(self.image)

        self.attack_damage_per_second = 30
        # to make the damage output non-affected by framerate adjustments
        self.attack_damage_per_frame = self.attack_damage_per_second / fps

    def tick(self):
        # get list from the file once and for all for this aim
        Enemy_list = ingame_level_data.Ingame_data["Enemy_list"]
        Enemy_dead_list = ingame_level_data.Ingame_data["Enemy_dead_list"]

        for enemy in Enemy_list:
            # line collision check
            if enemy.rect.clipline((self.line_start, self.line_end)):
                enemy.health -= self.attack_damage_per_frame
                if enemy.health <= 0:
                    Enemy_list.remove(enemy)
                    Enemy_dead_list.add(enemy)

            #  pixel collision check
        #      if self.linear_mask.overlap(enemy.enemy_mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
        #         enemy.health -= self.attack_damage_per_frame
        #        # if Enemy is dead
        #       if enemy.health <= 0:
        #          Enemy_list.remove(enemy)
        #         Enemy_dead_list.add(enemy)
        self.kill()
