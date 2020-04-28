# Projekt zaliczeniowy JS - Bartosz Knapik
import pygame as pg
import random
import os

# game constants
TITLE = 'SPACE RUN'
WIDTH = 800
HEIGHT = 600
FPS = 60
POWER_UP_TIME = 5000
HIGHSCORE_FILE = "highscores.dat"

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)

# paths
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
fonts_folder = os.path.join(game_folder, 'fonts')
sounds_folder = os.path.join(game_folder, 'sounds')

def draw_text(surface, font, pos, text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if pos == 'midtop':
        text_rect.midtop = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def show_menu(score):
    screen.blit(background, background_rect)
    draw_text(screen, title_font, 'midtop', TITLE, WHITE, WIDTH / 2, 80)
    draw_text(screen, small_font, 'midtop', 'Press SPACE to play', BLUE, WIDTH / 2, 240)
    # load highscores
    with open(os.path.join(game_folder, HIGHSCORE_FILE), 'r') as f:
        highscore = int(f.read())
    if score > highscore:
        draw_text(screen, medium_font, 'midtop', 'NEW HIGHSCORE:  ' + str(score), WHITE, WIDTH / 2, 340)
        with open(os.path.join(game_folder, HIGHSCORE_FILE), 'w') as f:
            f.write(str(score))
    else:
        draw_text(screen, medium_font, 'midtop', 'HIGHSCORE:  ' + str(highscore), WHITE, WIDTH / 2, 340)

    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    waiting = False

def spawn_enemy():
    e = Enemy()
    all_entities.add(e)
    enemies.add(e)

def draw_status_bar(surface, x, y, color, value):
    if value < 0:
        value = 0
    BAR_LENGTH = 180
    BAR_HEIGHT = 15
    fill = (value / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surface, color, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)

class Game:
    pass

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.life = 100
        self.power = 0
        self.power_time = pg.time.get_ticks()


    def update(self):
        self.speed_x = 0
        key_state = pg.key.get_pressed()
        if key_state[pg.K_d]:
            self.speed_x = 15
        if key_state[pg.K_a]:
            self.speed_x = -15
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # powerup timeout
        if self.power and pg.time.get_ticks() - self.power_time > POWER_UP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()

    def shoot(self):
        if self.power == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_entities.add(bullet)
            bullets.add(bullet)
            laser_sound.play()
        if self.power == 1:
            bullet_1 = Bullet(self.rect.left, self.rect.centery)
            bullet_2 = Bullet(self.rect.right, self.rect.centery)
            all_entities.add(bullet_1, bullet_2)
            bullets.add(bullet_1, bullet_2)
            laser_sound.play()

    def power_up(self):
        self.power = 1
        self.power_time = pg.time.get_ticks()

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_x = random.randrange(-3, 3)
        self.speed_y = random.randrange(1, 8)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation += (self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 20 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'laser'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 6

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

# initialize pygame, create game window
pg.init
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('SPACE RUN')
icon = pg.image.load(os.path.join(img_folder, 'icon.png'))
pg.display.set_icon(icon)
clock = pg.time.Clock()

# load all images
menu_bg = pg.image.load(os.path.join(img_folder, 'menu_bg.png')).convert()
menu_bg_rect = menu_bg.get_rect()
background = pg.image.load(os.path.join(img_folder, 'background.png')).convert()
background_rect = background.get_rect()
player_img = pg.image.load(os.path.join(img_folder, 'player.png')).convert()
bullet_img = pg.image.load(os.path.join(img_folder, 'laser.png')).convert()
meteor_images = []
meteor_list = ['meteorite_small.png', 'meteorite_medium.png', 'meteorite_big.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(os.path.join(img_folder, img)).convert())
powerup_images = {}
powerup_images['hp'] = pg.image.load(os.path.join(img_folder, 'powerup_hp.png')).convert()
powerup_images['laser'] = pg.image.load(os.path.join(img_folder, 'powerup_laser.png')).convert()

# load fonts
small_font = pg.font.Font(os.path.join(fonts_folder, 'sterilict.ttf'), 20)
medium_font = pg.font.Font(os.path.join(fonts_folder, 'sterilict.ttf'), 30)
title_font = pg.font.Font(os.path.join(fonts_folder, 'dustifine.ttf'), 80)

# load sounds
laser_sound = pg.mixer.Sound(os.path.join(sounds_folder, 'laser.wav'))
power_up_hp_sound = pg.mixer.Sound(os.path.join(sounds_folder, 'powerup_hp.wav'))
power_up_laser_sound = pg.mixer.Sound(os.path.join(sounds_folder, 'powerup_laser.wav'))
hit_sounds = []
for snd in ['hit1.wav', 'hit2.wav']:
    hit_sounds.append(pg.mixer.Sound(os.path.join(sounds_folder, snd)))
pg.mixer.music.load(os.path.join(sounds_folder, 'soundtrack.mp3'))

bg_y1 = 0
bg_y2 = -HEIGHT
score_tmp = 0

pg.mixer.music.play(loops = -1)
# main game loop
game_over = True
running = True
while running:
    if game_over:
        show_menu(score_tmp)
        game_over = False
        all_entities = pg.sprite.Group()
        enemies = pg.sprite.Group()
        bullets = pg.sprite.Group()
        powerups = pg.sprite.Group()
        player = Player()
        all_entities.add(player)

        for i in range(20):
            spawn_enemy()

        score = 0

    clock.tick(FPS)
    # events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()

    # update
    all_entities.update()

    # collision
    hits = pg.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 1
        random.choice(hit_sounds).play()
        if random.random() > 0.9:
            powerup = PowerUp(hit.rect.center)
            all_entities.add(powerup)
            powerups.add(powerup)
        spawn_enemy()

    hits = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
    for hit in hits:
        player.life -= hit.radius * 2
        spawn_enemy()
        if player.life <= 0:
            score_tmp = score
            game_over = True

    hits = pg.sprite.spritecollide(player, powerups, True)
    pup_time = 2 * (pg.time.get_ticks() - player.power_time) / 100
    for hit in hits:
        if hit.type == 'hp':
            power_up_hp_sound.play()
            player.life += 20
            if player.life >= 100:
                player.life = 100
        if hit.type == 'laser':
            power_up_laser_sound.play()
            player.power_up()
    # draw
    screen.fill(BLACK)
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))
    bg_y1 += 4
    bg_y2 += 4
    if bg_y1 > HEIGHT:
        bg_y1 = 0
    if bg_y2 > 0:
        bg_y2 = -HEIGHT

    all_entities.draw(screen)
    draw_text(screen, small_font, 'midtop', 'score  ' + str(score), WHITE, WIDTH / 2, 10)
    draw_text(screen, small_font, 'topleft', 'life ', WHITE, 10, 10)
    draw_status_bar(screen, 70, 12, GREEN, player.life)
    if player.power:
        draw_text(screen, small_font, 'topleft', 'UP ', WHITE, 10, 32)
        draw_status_bar(screen, 70, 32, BLUE, (100 - (pup_time)))
    pg.display.flip()

pg.quit()
quit()