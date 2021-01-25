import pygame
import sys
import os


size = width, height = 800, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
c = 0


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def win1():
    background = load_image('next.jpg')
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def win2():
    background = load_image('win.jpg')
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def gameover():
    background = load_image('gameover.png')
    screen.blit(background, (70, 30))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(fps)


def start_screen():
    text = ['НАКОРМИ УТКУ',
            '',
            'Правила игры:',
            'Кушай кукурузу,',
            'Не ешь хлеб']

    background = load_image('fon.jpg')
    screen.blit(background, (0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in text:
        string = font.render(line, 1, pygame.Color('blue'))
        string_rect = string.get_rect()
        text_coord = text_coord + 40
        string_rect.top = text_coord
        string_rect.x = 300
        text_coord = text_coord + string_rect.height
        screen.blit(string, string_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(fps)


def load_level(name):
    fullname = name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)

    return level_map


def draw_level(level_map):
    new_player = None
    x = None
    y = None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('trava.png', x, y)
            elif level_map[y][x] == '#':
                Tile('yachik.png', x, y)
            elif level_map[y][x] == '@':
                Tile('trava.png', x, y)
                new_player = Player(x, y)
            elif level_map[y][x] == '&':
                Tile('trava.png', x, y)
                brokoli = Brokoli(x, y)
            elif level_map[y][x] == '*':
                Tile('trava.png', x, y)
                xleb = Xleb(x, y)
            elif level_map[y][x] == '(':
                Tile('trava.png', x, y)
                xleb2 = Xleb2(x, y)
            elif level_map[y][x] == '!':
                Tile('trava.png', x, y)
                brokoli2 = Brokoli2(x, y)
            elif level_map[y][x] == '%':
                Tile('trava.png', x, y)
                brokoli3 = Brokoli3(x, y)
            elif level_map[y][x] == ')':
                Tile('trava.png', x, y)
                xleb3 = Xleb3(x, y)
            elif level_map[y][x] == '?':
                Tile('trava.png', x, y)
                xleb4 = Xleb4(x, y)

    return new_player, x, y, brokoli, xleb, xleb2, brokoli2, brokoli3, xleb3, xleb4


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile_type)
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

        self.add(tiles_group, all_sprites)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('utka.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x + 10, 50 * pos_y)

        self.add(player_group, all_sprites)

        self.wallcoords = [(10, 50), (210, 100), (260, 100), (310, 100),
                           (360, 100), (410, 100), (460, 100), (510, 100),
                           (560, 100), (660, 150), (710, 150), (760, 150),
                           (160, 150), (110, 150), (60, 150), (10, 150),
                           (210, 150), (210, 200),
                           (260, 200), (310, 200), (360, 200), (360, 250),
                           (410, 250), (460, 250), (510, 250),
                           (60, 250), (110, 250), (360, 350),
                           (310, 350), (260, 350), (210, 350), (210, 300),
                           (160, 300), (110, 300), (510, 350),
                           (560, 350), (660, 350), (710, 350), (710, 300),
                           (710, 250), (610, 350), (110, 400),
                           (10, 300), (760, 300)]
        self.wallcoords2 = [(360, 200), (310, 200), (410, 200), (460, 200),
                            (510, 200), (10, 300), (60, 300),
                            (110, 300),
                            (160, 300), (210, 300), (210, 350), (260, 350),
                            (310, 350), (360, 350), (410, 350),
                            (460, 350),
                            (510, 350), (660, 350),
                            (710, 350), (760, 350), (760, 300), (760, 250),
                            (660, 250), (660, 200), (660, 150),
                            (710, 150), (10, 50), (260, 50), (260, 100),
                            (310, 100), (360, 100), (410, 100),
                            (510, 100), (160, 150), (110, 150), (10, 150),
                            (210, 250), (160, 250), (110, 250),
                            (510, 300),
                            (760, 150), (510, 50), (510, 250)]

    def move_up(self):
        if self.rect[1] > 50 and (self.rect[0], self.rect[1]-50) not in self.wallcoords:
            self.rect = self.rect.move(0, -50)

    def move_down(self):
        if self.rect[1] < 400 and (self.rect[0], self.rect[1]+50) not in self.wallcoords:
            self.rect = self.rect.move(0, +50)

    def move_left(self):
        if self.rect[0] > 50 and (self.rect[0]-50, self.rect[1]) not in self.wallcoords:
            self.rect = self.rect.move(-50, 0)

    def move_reight(self):
        if self.rect[0] < 750 and (self.rect[0]+50, self.rect[1]) not in self.wallcoords:
            self.rect = self.rect.move(+50, 0)

    def move_up2(self):
        if self.rect[1] > 50 and (self.rect[0], self.rect[1]-50) not in self.wallcoords2:
            self.rect = self.rect.move(0, -50)

    def move_down2(self):
        if self.rect[1] < 400 and (self.rect[0], self.rect[1]+50) not in self.wallcoords2:
            self.rect = self.rect.move(0, +50)

    def move_left2(self):
        if self.rect[0] > 50 and (self.rect[0]-50, self.rect[1]) not in self.wallcoords2:
            self.rect = self.rect.move(-50, 0)

    def move_reight2(self):
        if self.rect[0] < 750 and (self.rect[0]+50, self.rect[1]) not in self.wallcoords2:
            self.rect = self.rect.move(+50, 0)


class Brokoli(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('kuk.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(brokoli_group, all_sprites)


class Brokoli2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('kuk.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(brokoli2_group, all_sprites)


class Brokoli3(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('kuk.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(brokoli3_group, all_sprites)


class Xleb2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('xleb.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(xleb2_group, all_sprites)


class Xleb3(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('xleb.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(xleb3_group, all_sprites)


class Xleb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('xleb.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(xleb_group, all_sprites)


class Xleb4(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('xleb.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(xleb4_group, all_sprites)


def level1():
    player, level_x, level_y, brokoli, xleb, xleb2, brokoli2, brokoli3, xleb3, \
                        xleb4 = draw_level(load_level('level.txt'))
    global c

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_UP or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_w:
                player.move_up()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_DOWN or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_s:
                player.move_down()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_LEFT or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_a:
                player.move_left()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_RIGHT or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_d:
                player.move_reight()
        if not pygame.sprite.collide_rect(player, xleb) and\
                not pygame.sprite.collide_rect(player, xleb2) and\
                not pygame.sprite.collide_rect(player, xleb3) and\
                not pygame.sprite.collide_rect(player, xleb4):

            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            brokoli_group.draw(screen)
            brokoli2_group.draw(screen)
            brokoli3_group.draw(screen)
            xleb_group.draw(screen)
            xleb2_group.draw(screen)
            xleb3_group.draw(screen)
            xleb4_group.draw(screen)
        else:
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            brokoli_group.empty()
            brokoli2_group.empty()
            brokoli3_group.empty()
            xleb_group.empty()
            xleb2_group.empty()
            xleb3_group.empty()
            xleb4_group.empty()
            gameover()

        if not pygame.sprite.collide_rect(player, brokoli) and \
                not pygame.sprite.collide_rect(player, brokoli2) and \
                not pygame.sprite.collide_rect(player, brokoli3):

            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            brokoli_group.draw(screen)
            brokoli2_group.draw(screen)
            brokoli3_group.draw(screen)
            xleb_group.draw(screen)
            xleb2_group.draw(screen)
            xleb3_group.draw(screen)
            xleb4_group.draw(screen)
        else:
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            brokoli_group.empty()
            brokoli2_group.empty()
            brokoli3_group.empty()
            xleb_group.empty()
            xleb2_group.empty()
            xleb3_group.empty()
            xleb4_group.empty()
            win1()
            level2()

        pygame.display.flip()
        clock.tick(fps)


def level2():
    player, level_x, level_y, brokoli, xleb, xleb2, brokoli2, brokoli3, xleb3,\
        xleb4 = draw_level(load_level('level2.txt'))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_UP or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_w:
                player.move_up2()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_DOWN or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_s:
                player.move_down2()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_LEFT or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_a:
                player.move_left2()

            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_RIGHT or\
                    event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_d:
                player.move_reight2()

            if not pygame.sprite.collide_rect(player, xleb) and \
                    not pygame.sprite.collide_rect(player, xleb2) and \
                    not pygame.sprite.collide_rect(player, xleb3) and\
                    not pygame.sprite.collide_rect(player, xleb4):

                screen.fill(pygame.Color(0, 0, 0))
                tiles_group.draw(screen)
                player_group.draw(screen)
                brokoli_group.draw(screen)
                brokoli2_group.draw(screen)
                brokoli3_group.draw(screen)
                xleb_group.draw(screen)
                xleb2_group.draw(screen)
                xleb3_group.draw(screen)
                xleb4_group.draw(screen)
            else:
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                brokoli_group.empty()
                brokoli2_group.empty()
                brokoli3_group.empty()
                xleb_group.empty()
                xleb2_group.empty()
                xleb3_group.empty()
                xleb4_group.empty()
                gameover()

            if not pygame.sprite.collide_rect(player, brokoli) and \
                    not pygame.sprite.collide_rect(player, brokoli2) and \
                    not pygame.sprite.collide_rect(player, brokoli3):

                screen.fill(pygame.Color(0, 0, 0))
                tiles_group.draw(screen)
                player_group.draw(screen)
                brokoli_group.draw(screen)
                brokoli2_group.draw(screen)
                brokoli3_group.draw(screen)
                brokoli3_group.draw(screen)
                xleb_group.draw(screen)
                xleb2_group.draw(screen)
                xleb3_group.draw(screen)
                xleb4_group.draw(screen)
            else:
                all_sprites.empty()
                tiles_group.empty()
                player_group.empty()
                brokoli_group.empty()
                brokoli2_group.empty()
                brokoli3_group.empty()
                xleb_group.empty()
                xleb2_group.empty()
                xleb3_group.empty()
                xleb4_group.empty()
                win2()
                terminate()

            pygame.display.flip()
            clock.tick(fps)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

brokoli_group = pygame.sprite.Group()
brokoli2_group = pygame.sprite.Group()
brokoli3_group = pygame.sprite.Group()

xleb_group = pygame.sprite.Group()
xleb2_group = pygame.sprite.Group()
xleb3_group = pygame.sprite.Group()
xleb4_group = pygame.sprite.Group()

start_screen()
level1()
terminate()