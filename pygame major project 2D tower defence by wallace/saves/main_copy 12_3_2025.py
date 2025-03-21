# initialising
import pygame
from classes.enemy import Enemy
from pygame.math import Vector2
import config

# start pygame
pygame.init()

# initialise icon and title
pygame.display.set_icon(pygame.image.load('../assets/game-icon.png'))
pygame.display.set_caption("Maths defence")

# get data from config file
screen = config.screen
fps = config.fps
tower_testIMG = config.tower_testIMG
enemy_snakeIMG = config.enemy_snakeIMG
bullet_IMG = config.bullet_IMG
player_health_font = config.player_health_font

# list for enemies prepared to spawn
Enemy_prep_list = pygame.sprite.Group()
# list for enemies spawned and are still on the screen
Enemy_list = pygame.sprite.Group()
#
Enemy_dead_list = pygame.sprite.Group()
# list of attacks
Attack_list = pygame.sprite.Group()


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
        # the direction this attack will go
        self.hit_list = None
        self.East = pygame.math.Vector2(1, 0)
        # clockwise angle from East axis
        self.angle = direction.angle_to(self.East)
        self.location = location

        self.image = pygame.transform.rotate(bullet_IMG, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.location

        # creating a mask for pixel perfect collision check
        self.linear_mask = pygame.mask.from_surface(self.image)

        self.attack_damage_per_second = 30
        # to make the damage output non-affected by framerate adjustments
        self.attack_damage_per_frame = self.attack_damage_per_second / fps

    def tick(self):
        for enemy in Enemy_list:
            # check if collided
            if self.linear_mask.overlap(enemy.enemy_mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
                enemy.health -= self.attack_damage_per_frame
      #          print(enemy.health)    #   show health after hit
                # if Enemy is dead
                if enemy.health <= 0:
                    Enemy_list.remove(enemy)
                    Enemy_dead_list.add(enemy)
        self.kill()


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
        # check the tower should aim at enemy
        if self.targeted_enemy is None and Enemy_list is not None:
            for active_enemy in Enemy_list:
                # OT - OE = ET
                # find the closest enemy (to tower)
                if self.targeted_enemy is None:
                    # make the enemy be the target if all other checked enemy is not in range
                    if (self.location - active_enemy.location).length() <= self.range:
                        self.targeted_enemy = active_enemy
                        # so this calculation does not need to be run everytime
                        self.distance_between_target_and_tower = (self.location - active_enemy.location).length()
                elif (self.location - active_enemy.location).length() < self.distance_between_target_and_tower:
                    # the enemy is closer to the tower than the previous target
                    self.targeted_enemy = active_enemy

        # check if there is a targeted enemy, is it dead
        if self.targeted_enemy is not None and self.targeted_enemy in Enemy_list:
            # check if it is in not range or has reached the end
            if (self.location - self.targeted_enemy.location).length() > self.range or self.targeted_enemy.location == self.targeted_enemy.checkpoints[-1]:
                self.targeted_enemy = None
            else:
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
            # enemy should not be targeted
            self.targeted_enemy = None

    def shoot(self):
        pass


class linear(Tower):
    def __init__(self, tower_type, level, location: Vector2):
        super().__init__(tower_type, level, location)
        self.range = 350

    def shoot(self):
        Attack_list.add(linear_attack(self.facing_vector, self.location))


# with the format of "level1" for the level parameter
def generate_enemies(level):
    for enemy_type in config.Level_preset[level]["enemy_data"]:
        # position of the enemy in the list of spawn time of its own type
        for spawn_time in config.Level_preset[level]["enemy_data"][enemy_type]["spawn_time"]:
            a = Enemy(enemy_type, level, spawn_time)
            Enemy_prep_list.add(a)


def display_player_health(player_health):
    show_health = player_health_font.render(f"Health: {player_health}", True, (255, 255, 255))
    # draw it at left bottom corner with a 10px padding
    screen.blit(show_health, (10, 490))


Tower_list = pygame.sprite.Group()


def place_tower(tower_type, level, location: Vector2):
    if tower_type == "linear":
        Tower_list.add(linear(tower_type, level, location))


config.Saved_data["current_health"] = 100

generate_enemies("level1")

background = config.Level_preset["level1"]["background_image"]

# Game loop
running = True

# initialise time right before the loop begins to avoid the delay from running other codes
clock = pygame.time.Clock()

# where level 0 is the homepage and level 1 will be battle places.
level_selected = 0

while running:
    match level_selected:
        case 0:
            screen.fill((232, 185, 77))

            pygame.draw.rect(screen, (0, 200, 0), [100, 100, 50, 50])

            # function to exit the game while player pressed X on game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # testing mouse
                    mouse = pygame.mouse.get_pos()
                    if 100 <= mouse[0] <= 150 and 100 <= mouse[1] <= 150:
                        level_selected = 1

            pygame.display.update()
            clock.tick(fps)

        case 1:
            # insert background image
            screen.blit(background, (0, 0))

            # display player health
            display_player_health(round(config.Saved_data["current_health"]))

            # function to exit the game while player pressed X on game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    place_tower("linear", "level1", Vector2(pygame.mouse.get_pos()))

                    # home & pause button
                    if 874 <= mouse[0] <= 940 and 0 <= mouse[1] <= 66:
                        level_selected = 0

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
            time = pygame.time.get_ticks() / 1000
            for enemy in Enemy_prep_list:
                if time >= enemy.spawn_time:
                    Enemy_prep_list.remove(enemy)
                    Enemy_list.add(enemy)

            # check if the player have any health left
            if config.Saved_data["current_health"] <= 0:
                running = False

            pygame.draw.rect(screen, (0, 200, 0), [874, 0, 66, 66])

            # put the changed things on screen
            pygame.display.update()
            clock.tick(fps)
pygame.quit()
