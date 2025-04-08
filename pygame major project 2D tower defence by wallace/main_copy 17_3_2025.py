# initialising
import pygame
from classes.enemy import Enemy
from pygame.math import Vector2
import config
from datetime import datetime
import ingame_level_data

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
        self.line_start = self.location + self.direction.normalize()*1090
        self.line_end = self.location - self.direction.normalize()*1090

        # creating a mask for pixel perfect collision check
        self.linear_mask = pygame.mask.from_surface(self.image)

        self.attack_damage_per_second = 30
        # to make the damage output non-affected by framerate adjustments
        self.attack_damage_per_frame = self.attack_damage_per_second / fps

    def tick(self):
        for enemy in Enemy_list:
            # try  collision with line
            if enemy.rect.clipline((self.line_start, self.line_end)):
                enemy.health -= self.attack_damage_per_frame
                if enemy.health <= 0:
                    Enemy_list.remove(enemy)
                    Enemy_dead_list.add(enemy)

            #  pixel collided
      #      if self.linear_mask.overlap(enemy.enemy_mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
       #         enemy.health -= self.attack_damage_per_frame
        #        # if Enemy is dead
         #       if enemy.health <= 0:
          #          Enemy_list.remove(enemy)
           #         Enemy_dead_list.add(enemy)
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
            ingame_level_data.Ingame_data["current_player_health"] = 200
            ingame_level_data.Ingame_data["current_player_health"] = config.Level_preset["level1"]["player_health"]
            generate_enemies("level1")
            background = config.Level_preset["level1"]["background_image"]
            tower_placed = 0

            # The enemies spawn relative to when the
            time_level_init = pygame.time.get_ticks()/1000

            # start loop for level 1
            while level1_running:
                # test for the actual time taken per frame
                start_time = datetime.now()


                # insert background image
                screen.blit(background, (0, 0))

                # display player health
                display_player_health(round(ingame_level_data.Ingame_data["current_player_health"]))

                # function to exit the game while player pressed X on game window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        level1_running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        place_tower("linear", "level1", Vector2(pygame.mouse.get_pos()))
                        tower_placed += 1

                        # home & reset button
                        if 874 <= mouse[0] <= 940 and 0 <= mouse[1] <= 66:
                            level_selected = 0
                            level1_running = False
                            Enemy_dead_list.empty()
                            Enemy_list.empty()
                            Enemy_prep_list.empty()
                            Tower_list.empty()

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

                pygame.draw.rect(screen, (0, 200, 0), [874, 0, 66, 66])

                # put the changed things on screen
                pygame.display.update()

                print(datetime.now() - start_time, "tower placed:", tower_placed)
                clock.tick(fps)

pygame.quit()
