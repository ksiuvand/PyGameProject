import pygame
import sys
import os

size = width, height = 800, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60


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


def start_screen():
    text = ['НАКОРМИ УТКУ',
            '',
            'Правила игры:',
            'Ешь броколи не ешь хлеб']

    background = load_image('fon.jpg')
    screen.blit(background, (0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in text:
        string = font.render(line, 1, pygame.Color('red'))
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
    new_player, x, y = None, None, None
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
                Tile('xleb.png', x, y)
                xleb = Xleb(x, y)

    return new_player, x, y, brokoli, xleb


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

    def move_up(self):
        self.rect = self.rect.move(0, -50)

    def move_down(self):
        self.rect = self.rect.move(0, +50)

    def move_left(self):
        self.rect = self.rect.move(-50, 0)

    def move_reight(self):
        self.rect = self.rect.move(+50, 0)


class Brokoli(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('brokoli.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(brokoli_group, all_sprites)


class Xleb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('xleb.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)

        self.add(xleb_group, all_sprites)


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx

        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width

        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy

        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def level1():
    player, level_x, level_y, brokoli, xleb = draw_level(load_level('level.txt'))
    camera = Camera((level_x, level_y))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_reight()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_reight()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_left()

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        if pygame.sprite.groupcollide(player_group, xleb_group, False, False):
            gameover = load_image('green.png')
            screen.blit(gameover, (75, 100))
        elif not pygame.sprite.collide_rect(player, brokoli):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            brokoli_group.draw(screen)
            xleb_group.draw(screen)
        else:
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            brokoli_group.empty()
            return

        pygame.display.flip()
        clock.tick(fps)


def level2():
    player, level_x, level_y, brokoli, xleb = draw_level(load_level('level2.txt'))
    #camera = Camera((level_x, level_y))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_reight()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_reight()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_left()

        #camera.update(player)
        #for sprite in all_sprites:
         #   camera.apply(sprite)

        if pygame.sprite.groupcollide(player_group, xleb_group, False, False):
            gameover = load_image('green.png')
            screen.blit(gameover, (75, 100))
        else:
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            brokoli_group.draw(screen)
            xleb_group.draw(screen)
            pygame.display.flip()
            clock.tick(fps)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
brokoli_group = pygame.sprite.Group()
xleb_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()

start_screen()
level1()
level2()
terminate()


