import pygame
import config
import ingame_level_data

# get global data from config
screen = config.Initialise["screen"]
currency = ingame_level_data.Ingame_data["current_player_currency"] 
big_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], config.Initialise["player_currency_font"][1], config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])
small_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], round(config.Initialise["player_currency_font"][1] / 2), config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])



# use the defined sprite class for its functions
class Shop_item():
    def __init__(self, position_in_list : int, level: int):

        # get defined data from input
        ##################################################################################
        self.position_in_list = position_in_list # position in the preset list, starting from 0
        # in format of "levelx" , x is an integer
        self.level = level

        # get the data according to the position
        ##################################################################################
        self.original_tower_image = config.Level_preset[self.level]["shop_data"][self.position_in_list][0]
        self.tower_image = config.Level_preset[self.level]["shop_data"][self.position_in_list][0]
        self.name: str = config.Level_preset[self.level]["shop_data"][self.position_in_list][1]
        self.description = config.Level_preset[self.level]["shop_data"][self.position_in_list][2]
        self.unlocked = config.Level_preset[self.level]["shop_data"][self.position_in_list][3]
        self.price = config.Level_preset[self.level]["shop_data"][self.position_in_list][4]

        # set common data for all shop items
        ##################################################################################
        # initially starts as top of the shop colum, y axis increases as number of shop items increase
        # all ## are done in the resize part, not need in initial
        ## self.rect = (740, 60 + 80 * self.position_in_list, 195, 70)
        ##self.x = self.rect[0]
        ##self.y = self.rect[1]

        # inner rect
        ## self.inner_rect = (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10)

        # shop item image
        ## self.tower_image_x = self.x + 10
        ## self.tower_image_y = self.y + 10

        # name
        ## self.name_x = self.x + 50
        ## self.name_y = self.tower_image_y
        ## self.show_name = big_font.render(self.name , True, (255, 255, 255))

        # description
        ## self.description_x = self.tower_image_x
        ## self.description_y = self.y + 50
        ## self.show_description = small_font.render(self.description , True, (255, 255, 255))

        ## self.price_x = self.x + 100
        ## self.price_y = self.y + 40
        ## self.show_price = big_font.render(str(self.price) , True, (255, 255, 0))


    def draw(self):
        pygame.draw.rect(screen, (102, 51, 0), pygame.Rect(self.rect))
        pygame.draw.rect(screen, (153, 102, 0), pygame.Rect(self.inner_rect))
        screen.blit(self.tower_image, (self.tower_image_x , self.tower_image_y))
        screen.blit(self.show_name, (self.name_x, self.name_y))
        screen.blit(self.show_description, (self.description_x, self.description_y))
        screen.blit(self.show_price, (self.price_x, self.price_y))

    def resize(self, resize_factor):
        self.tower_image = pygame.transform.scale_by(self.original_tower_image, resize_factor)

        self.rect = (740 * resize_factor, float(60 + 80 * self.position_in_list) * resize_factor, 195 * resize_factor, 70 * resize_factor)
        self.x = self.rect[0]
        self.y = self.rect[1]

        # shop item image
        self.tower_image_x = self.x + (10 * resize_factor)
        self.tower_image_y = self.y + (10 * resize_factor)

        self.inner_rect = (self.rect[0] + (5 * resize_factor), self.rect[1] + (5 * resize_factor), self.rect[2] - (10 * resize_factor), self.rect[3] - (10 * resize_factor))

        # texts
        big_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], round(config.Initialise["player_currency_font"][1] * resize_factor), config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])
        small_font = pygame.font.SysFont(config.Initialise["player_currency_font"][0], round(config.Initialise["player_currency_font"][1] * resize_factor / 2), config.Initialise["player_currency_font"][2], config.Initialise["player_currency_font"][3])
    
        self.name_x = self.x + (50 * resize_factor)
        self.name_y = self.tower_image_y
        self.show_name = big_font.render(self.name , True, (255, 255, 255))

        self.description_x = self.tower_image_x
        self.description_y = self.y + (50 * resize_factor)
        self.show_description = small_font.render(self.description , True, (255, 255, 255))

        self.price_x = self.x + (100 * resize_factor)
        self.price_y = self.y + (40 * resize_factor)
        self.show_price = big_font.render(str(self.price) , True, (255, 255, 0))

    def check_press(self, mouse_pos):
        # check if pressed on this item
        if self.x <= mouse_pos[0] <= (self.x + self.rect[2]) and self.y <= mouse_pos[1] <= (self.y + self.rect[3]):
            return True
        else: return False