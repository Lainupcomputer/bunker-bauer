import pygame, sys
import json


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # ground
        self.ground_surface = pygame.image.load('gfx/basic/background.png').convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(topleft=(0, 0))

        self.display_surface = pygame.display.get_surface()
        self.camera_borders = {'left': 50, 'right': 50, 'top': 50, 'bottom': 50}
        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # mouse speed
        self.mouse_speed = 5

        # Play field
        self.border_right = 4000
        self.border_bottom = 4000

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border, mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x, bottom_border))

        self.offset += mouse_offset_vector * self.mouse_speed

        # border right
        if self.offset[0] >= self.border_right:
            self.offset[0] = self.border_right
        # border bottom
        if self.offset[1] > self.border_bottom:
            self.offset[1] = self.border_bottom

        if self.offset[0] <= 0:
            self.offset[0] = 0

        if self.offset[1] <= 0:
            self.offset[1] = 0

    def custom_draw(self):
        self.mouse_control()
        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surface, ground_offset)

        # elements active
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


class Game:
    def __init__(self):
        self.savegame = None
        self.update_cycle = 0
        # rooms
        # row 1
        self.room_1_1 = None
        self.room_1_2 = None
        self.room_1_3 = None
        self.room_1_4 = None
        self.room_1_5 = None
        # row 2
        self.room_2_1 = None
        self.room_2_2 = None
        self.room_2_3 = None
        self.room_2_4 = None
        self.room_2_5 = None

    def get_savegame(self):
        with open("savegame.json", "r") as f:
            self.savegame = json.load(f)

    def save_savegame(self, file):
        with open("savegame.json", "w") as f:
            json.dump(file, f, indent=2)

    def update(self):
        screen.fill('#71ddee')
        camera_group.update()
        camera_group.custom_draw()

        if self.update_cycle == 0:
            # update cycle
            self.init_rooms()

        hud.set()
        hud.draw()
        self.handle_events()

        self.update_cycle += 1
        if self.update_cycle >= 60:
            self.update_cycle = 0
        clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pressed = True
                    mouse_position = pygame.mouse.get_pos()
                    relative_mouse_position = (mouse_position[0] + camera_group.offset.x,
                                               mouse_position[1] + camera_group.offset.y)
                    while pressed:
                        # bottom right buttons
                        if hud.inventory_button.collidepoint(mouse_position):
                            print("hud:inventory")
                        # rooms
                        if self.room_1_1.rect.collidepoint(relative_mouse_position):
                            print("room1-1")
                        if self.room_1_2.rect.collidepoint(relative_mouse_position):
                            print("room2-1")
                        if self.room_1_3.rect.collidepoint(relative_mouse_position):
                            print("room3-1")
                        if self.room_1_4.rect.collidepoint(relative_mouse_position):
                            print("room4-1")
                        if self.room_1_5.rect.collidepoint(relative_mouse_position):
                            print("room5-1")
                        if self.room_2_1.rect.collidepoint(relative_mouse_position):
                            print("room1-2")
                        if self.room_2_2.rect.collidepoint(relative_mouse_position):
                            print("room2-2")
                        if self.room_2_3.rect.collidepoint(relative_mouse_position):
                            print("room3-2")
                        if self.room_2_4.rect.collidepoint(relative_mouse_position):
                            print("room4-2")
                        if self.room_2_5.rect.collidepoint(relative_mouse_position):
                            print("room5-2")



                        print(camera_group.offset)
                        print(pygame.mouse.get_pos())
                        print(f" click pos: {relative_mouse_position}")

                        pressed = False

    def handle_buttons(self):
        pass

    def init_rooms(self):
        game.get_savegame()
        row_1 = game.savegame["savegame"]["map"]["row_1"]
        row_2 = game.savegame["savegame"]["map"]["row_2"]

        self.room_1_1 = Room((row_1["tile_1"]["position_x"], row_1["position_y"]), camera_group,
                             game.savegame["savegame"]["map"]["row_1"]["tile_1"])
        self.room_1_2 = Room((row_1["tile_2"]["position_x"], row_1["position_y"]), camera_group,
                             game.savegame["savegame"]["map"]["row_1"]["tile_2"])
        self.room_1_3 = Room((row_1["tile_3"]["position_x"], row_1["position_y"]), camera_group,
                             game.savegame["savegame"]["map"]["row_1"]["tile_3"])
        # self.room_1_4 = Room((row_1["tile_4"]["position_x"], row_1["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_1"]["tile_4"])
        # self.room_1_5 = Room((row_1["tile_5"]["position_x"], row_1["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_1"]["tile_5"])
        #
        # self.room_2_1 = Room((row_2["tile_1"]["position_x"], row_2["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_2"]["tile_1"])
        # self.room_2_2 = Room((row_2["tile_2"]["position_x"], row_2["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_2"]["tile_2"])
        # self.room_2_3 = Room((row_2["tile_3"]["position_x"], row_2["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_2"]["tile_3"])
        # self.room_2_4 = Room((row_2["tile_4"]["position_x"], row_2["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_2"]["tile_4"])
        # self.room_2_5 = Room((row_2["tile_5"]["position_x"], row_2["position_y"]), camera_group,
        #                      game.savegame["savegame"]["map"]["row_2"]["tile_5"])


class Room(pygame.sprite.Sprite):
    def __init__(self, pos, group, id):
        super().__init__(group)
        self.group_id = id
        self.image_path = ""
        # status
        self.status = self.group_id['status']
        print(self.status)

        if self.status == "not_owned":
            self.image_path = "gfx/game/room_empty_for-sale.png"
            self.price = self.group_id['price']

        if self.status == "construction":
            asset_folder = "gfx/game/room_building/"
            self.room = self.group_id['room']  # room to draw
            self.construction_stage = self.group_id['construction_stage']
            if self.construction_stage == -4:
                self.image_path = asset_folder + "1.png"  # Tile Bought
            elif self.construction_stage == -3:
                self.image_path = asset_folder + "2.png"  # Tile Framed
            elif self.construction_stage == -2:
                self.image_path = asset_folder + "3.png"  # Tile Wired
            elif self.construction_stage == -1:
                self.image_path = asset_folder + "4.png"  # Tile finish

        if self.status == "owned":
            self.room = self.group_id['room']  # room to draw
            self.construction_stage = self.group_id['construction_stage']  # lvl
            self.room_name = self.group_id['room_name']  # display name
            self.room_health = self.group_id['room_health']

            # get owned room
            if self.room == "entrance":  # entrance
                self.image_path = f"gfx/game/entrance/entrance{self.construction_stage}.png"

            if self.room == "reactor":  # energy room
                self.image_path = f"gfx/game/reactor/reactor{self.construction_stage}.png"

        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class HUD:
    def __init__(self, screen):
        self.font = pygame.font.SysFont("comicsansms", 15)
        self.custom_font = pygame.font.SysFont("comicsansms", 30)
        self.screen = screen

        # positions
        self.pos_bg = 250
        self.pos_bar = 255
        self.offset = 250

        # bar values
        self.bar_energy = 200
        self.bar_energy_max = 100
        self.bar_food = 200
        self.bar_food_max = 200
        self.bar_water = 200
        self.bar_water_max = 200

        # text values
        self.credits = 100
        self.mun = 100

        # buttons
        self.inventory_button = None
        self.crafting_button = None
        self.skills_button = None

    def draw(self, currency=True, top_bar=True, bottom_right=True):
        if currency:
            # Credits
            pygame.draw.rect(self.screen, (25, 25, 25), (1050, 15, 90, 30))  # draw background
            creds = self.font.render(f"{self.credits}", True, (155, 155, 155))
            credits_rect = creds.get_rect()
            credits_rect.topleft = (1060, 20)  # place
            self.screen.blit(creds, credits_rect)
            # Mun
            pygame.draw.rect(self.screen, (25, 25, 25), (1160, 15, 90, 30))  # draw background
            mun = self.font.render(f"{self.credits}", True, (155, 155, 155))
            mun_rect = mun.get_rect()
            mun_rect.topleft = (1170, 20)  # place
            self.screen.blit(mun, mun_rect)
        if top_bar:
            # energy
            pygame.draw.rect(self.screen, (25, 25, 25), (self.pos_bg, 15, 210, 30))  # draw background
            pygame.draw.rect(self.screen, (255, 0, 0), (self.pos_bar, 20, self.bar_energy, 20))  # draw bar
            energy_bar = self.font.render(f"{self.bar_energy}/{self.bar_energy_max}", True, (155, 155, 155))
            energy_bar_rect = energy_bar.get_rect()
            energy_bar_rect.topleft = (325, 20)  # place
            self.screen.blit(energy_bar, energy_bar_rect)
            # food
            pygame.draw.rect(self.screen, (25, 25, 25), (self.pos_bg + self.offset, 15, 210, 30))  # draw background
            pygame.draw.rect(self.screen, (255, 0, 0), (self.pos_bar + self.offset, 20, self.bar_food, 20))  # draw bar
            food_bar = self.font.render(f"{self.bar_food}/{self.bar_food_max}", True, (155, 155, 155))
            food_bar_rect = food_bar.get_rect()
            food_bar_rect.topleft = (325 + self.offset, 20)  # place
            self.screen.blit(food_bar, food_bar_rect)
            # water
            pygame.draw.rect(self.screen, (25, 25, 25), (self.pos_bg + self.offset * 2, 15, 210, 30))  # draw background
            pygame.draw.rect(self.screen, (255, 0, 0), (self.pos_bar + self.offset * 2, 20, self.bar_water, 20))  # draw bar
            water_bar = self.font.render(f"{self.bar_water}/{self.bar_water_max}", True, (155, 155, 155))
            water_bar_rect = water_bar.get_rect()
            water_bar_rect.topleft = (325 + self.offset * 2, 20)  # place
            self.screen.blit(water_bar, water_bar_rect)

        if bottom_right:
            # Inventory
            self.inventory_button = pygame.draw.rect(self.screen, (25, 25, 25), (1200, 650, 50, 50))  # draw background
            inventory_btn = self.custom_font.render(f"I", True, (155, 155, 155))
            inventory_btn_rect = inventory_btn.get_rect()
            inventory_btn_rect.topleft = (1215, 655)  # place
            self.screen.blit(inventory_btn, inventory_btn_rect)
            # Crafting
            self.crafting_button = pygame.draw.rect(self.screen, (25, 25, 25), (1200, 590, 50, 50))  # draw background
            crafting_btn = self.custom_font.render(f"C", True, (155, 155, 155))
            crafting_btn_rect = crafting_btn.get_rect()
            crafting_btn_rect.topleft = (1215, 595)  # place
            self.screen.blit(crafting_btn, crafting_btn_rect)
            # skills
            self.skills_button = pygame.draw.rect(self.screen, (25, 25, 25), (1200, 530, 50, 50))  # draw background
            skills_btn = self.custom_font.render(f"S", True, (155, 155, 155))
            skills_btn_rect = skills_btn.get_rect()
            skills_btn_rect.topleft = (1215, 535)  # place
            self.screen.blit(skills_btn, skills_btn_rect)

    def set(self, energy=(200, 200), food=(200, 200), water=(200, 200), creds=100, mun=100):  # Update Function
        self.bar_energy = energy[0]
        self.bar_energy_max = energy[1]
        self.bar_food = food[0]
        self.bar_food_max = food[1]
        self.bar_water = water[0]
        self.bar_water_max = water[1]
        self.credits = creds
        self.mun = mun


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("bunker-bauer")
clock = pygame.time.Clock()

camera_group = CameraGroup()
game = Game()
clicked_room = None

hud = HUD(screen)

while True:


    if clicked_room is not None:
        #screen.blit(pygame.image.load("gfx/basic/room_overlay.png"), (0, 0))
        print("done")


    game.update()
    pygame.display.update()

