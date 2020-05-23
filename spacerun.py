# Projekt zaliczeniowy JS - Bartosz Knapik


import os
import random

import pygame as pg

# Stałe projektu.

TITLE = 'SPACE RUN'
HIGHSCORE_FILE = "highscores.dat"
WIDTH = 800
HEIGHT = 600
FPS = 60
POWER_UP_TIME = 5000
BAR_LENGTH = 180
BAR_HEIGHT = 15
SMALL_FONT_SIZE = 20
MEDIUM_FONT_SIZE = 30
TITLE_FONT_SIZE = 80
ENEMIES_NUMBER = 40

# Kolory.

WHITE = pg.Color('#ffffff')
BLACK = pg.Color('#000000')
RED = pg.Color('#ac0103')
GREEN = pg.Color('#3bcb4f')
BLUE = pg.Color('#268bd2')
YELLOW = pg.Color('#b58900')

# Ścieżki:

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
fonts_folder = os.path.join(game_folder, 'fonts')
sounds_folder = os.path.join(game_folder, 'sounds')


class Game:
    """Główna klasa gry.

    Klasa inicjalizuje biblioteki, ładuje grafikę, czcionki i dźwięki używane w grze.
    Zawiera metody odpowiedzialne za rysowanie obiektów na ekranie (tekstu, grafiki).
    Obsługuje kolizję obiektów oraz koordynuje działanie gry.
    """
    pg.init
    pg.font.init()
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    pg.display.set_caption('SPACE RUN')

    # Wczytanie plików graficznych

    icon = pg.image.load(os.path.join(img_folder, 'icon.png'))
    pg.display.set_icon(icon)
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
    powerup_images = dict()
    powerup_images['hp'] = pg.image.load(os.path.join(img_folder, 'powerup_hp.png')).convert()
    powerup_images['laser'] = pg.image.load(os.path.join(img_folder, 'powerup_laser.png')).convert()

    # Wczytanie czcionek

    small_font = pg.font.Font(os.path.join(fonts_folder, 'sterilict.ttf'), SMALL_FONT_SIZE)
    medium_font = pg.font.Font(os.path.join(fonts_folder, 'sterilict.ttf'), MEDIUM_FONT_SIZE)
    title_font = pg.font.Font(os.path.join(fonts_folder, 'dustifine.ttf'), TITLE_FONT_SIZE)

    # Wczytanie dźwięków

    laser_sound = pg.mixer.Sound(os.path.join(sounds_folder, 'laser.wav'))
    power_up_hp_sound = pg.mixer.Sound(os.path.join(sounds_folder, 'powerup_hp.wav'))
    power_up_laser_sound = pg.mixer.Sound(os.path.join(sounds_folder, 'powerup_laser.wav'))
    hit_sounds = []
    for snd in ['hit1.wav', 'hit2.wav']:
        hit_sounds.append(pg.mixer.Sound(os.path.join(sounds_folder, snd)))
    pg.mixer.music.load(os.path.join(sounds_folder, 'soundtrack.mp3'))
    pg.mixer.music.play(loops=-1)

    PUP_CHANCE = 0.95  # Procentowa szansa na pojawienie się bonusu (100 - PUP_CHANCE)
    BG_SPEED = 4  # Szybkość przewijania tła gry

    def __init__(self):
        self.running = True
        self.game_over = True
        self.score = 0
        self.bg_y1 = 0
        self.bg_y2 = -HEIGHT
        self.all_entities = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.pup_time = 0
        self.player = None

    def draw_text(self, font, pos, text, color, x, y):
        """Metoda odpowiedzialna za wyświetlanie tekstu w oknie gry.

        Argumenty:
            font: Czcionka, której ma użyć funkcja do wyświetlenia napisu.
            pos: Pozycja tekstu na ekranie.
            text: Tekst do wyświetlenia.
            color: Kolor tekstu.
            x: Współrzędna "x" tekstu.
            y: Współrzędna "y" tekstu.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if pos == 'midtop':
            text_rect.midtop = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_menu(self):
        """Metoda odpowiedzialna za wyświetlanie ekranu startowego i wczytanie najlepszego wyniku."""
        self.screen.blit(self.background, self.background_rect)
        self.draw_text(self.title_font, 'midtop', TITLE, WHITE, WIDTH / 2, HEIGHT / 8)
        self.draw_text(self.small_font, 'midtop', 'Press SPACE to play . . .', BLUE, WIDTH / 2, HEIGHT / 3)
        self.draw_text(self.small_font, 'midtop', 'SPACE - shoot', RED, WIDTH / 2, HEIGHT / 2.2)
        self.draw_text(self.small_font, 'midtop', 'A , D - move', RED, WIDTH / 2, HEIGHT / 2)

        # Wczytanie najlepszego wyniku:

        with open(os.path.join(game_folder, HIGHSCORE_FILE), 'r') as f:
            highscore = int(f.read())
        if self.score > highscore:
            self.draw_text(self.medium_font, 'midtop', 'NEW HIGHSCORE:  ' + str(self.score), WHITE, WIDTH / 2,
                           HEIGHT / 1.5)
            with open(os.path.join(game_folder, HIGHSCORE_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text(self.medium_font, 'midtop', 'HIGHSCORE:  ' + str(highscore), WHITE, WIDTH / 2,
                           HEIGHT / 1.5)

        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def draw_status_bar(self, x, y, color, value):
        """Metoda odpowiadająca za wyświetlanie się paska statusu naszego bonusu (podwójny pocisk).

        Argumenty:
            x: Współrzędna "x" paska.
            y: Współrzędna "y" paska.
            color: Kolor wypełnienia paska.
            value: Poziom wypełnienia paska.
        """
        if value < 0:
            value = 0
        fill = (value / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(self.screen, color, fill_rect)
        pg.draw.rect(self.screen, WHITE, outline_rect, 2)

    def spawn_enemy(self):
        """Metoda odpowiadająca za pojawianie się wrogów."""
        e = Enemy(self)
        self.all_entities.add(e)
        self.enemies.add(e)

    def events(self):
        """Metoda obsługująca zdarzenia (strzelanie, wyjście z gry)."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot(self)

    def clean_up(self):
        """Metoda usuwa wszystkie jednostki z planszy."""
        for e in self.all_entities:
            e.kill()

    def collision(self):
        """Metoda obsługująca kolizję obiektów w grze i wykonująca odpowiednie akcje, zależne od rodzaju kolizji."""
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 1
            random.choice(self.hit_sounds).play()
            if random.random() > self.PUP_CHANCE:
                powerup = PowerUp(self, hit.rect.center)
                self.all_entities.add(powerup)
                self.powerups.add(powerup)
            self.spawn_enemy()

        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        self.pup_time = 2 * (pg.time.get_ticks() - self.player.power_time) / 100
        for hit in hits:
            if hit.type == 'hp':
                self.power_up_hp_sound.play()
                self.player.life += 20
                if self.player.life >= self.player.PLAYER_LIFE:
                    self.player.life = self.player.PLAYER_LIFE
            if hit.type == 'laser':
                self.power_up_laser_sound.play()
                self.player.power_up()

        hits = pg.sprite.spritecollide(self.player, self.enemies, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.life -= hit.radius * 2
            self.spawn_enemy()
            if self.player.life <= 0:
                self.game_over = True
                self.clean_up()

    def draw(self):
        """Metoda odpowiada za ciągłe przewijanie tła gry oraz wyświetlanie punktów, paska stanu zdrowia i bonusu."""
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, self.bg_y1))
        self.screen.blit(self.background, (0, self.bg_y2))
        self.bg_y1 += self.BG_SPEED
        self.bg_y2 += self.BG_SPEED
        if self.bg_y1 > HEIGHT:
            self.bg_y1 = 0
        if self.bg_y2 > 0:
            self.bg_y2 = -HEIGHT

        self.all_entities.draw(self.screen)
        self.draw_text(self.small_font, 'midtop', 'score  ' + str(self.score), WHITE, WIDTH / 2, 10)
        self.draw_text(self.small_font, 'topleft', 'life ', WHITE, 10, 10)
        self.draw_status_bar(70, 12, GREEN, self.player.life)
        if self.player.power:
            self.draw_text(self.small_font, 'topleft', 'UP ', WHITE, 10, 32)
            self.draw_status_bar(70, 32, BLUE, (100 - self.pup_time))
        pg.display.flip()

    def game_start(self):
        """Metoda inicjująca grę.

        Metoda ustawia gracza oraz odpowiednią ilość wrogich obiektów w oknie gry.
        """
        self.show_menu()
        self.game_over = False
        self.player = Player(self)
        self.all_entities.add(self.player)

        for i in range(ENEMIES_NUMBER):
            self.spawn_enemy()

        self.score = 0


class Player(pg.sprite.Sprite):
    """Klasa reprezentująca gracza."""

    PLAYER_SPEED = 15
    PLAYER_LIFE = 100

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = game.player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.life = self.PLAYER_LIFE
        self.power = 0
        self.power_time = pg.time.get_ticks()

    def update(self):
        """Metoda odpowiadająca za poruszanie się gracza.

        Metoda umożliwia poruszanie się statku poprzez wykrywanie wciśniętego przycisku przez gracza.
        Metoda zapobiega również wychodzeniu statku poza krawędzie okna gry.
        Metoda odpowiada także za wyłączenie bonusu podwójnego lasera po odpowiednim czasie.
        """
        self.speed_x = 0
        key_state = pg.key.get_pressed()
        if key_state[pg.K_d]:
            self.speed_x = self.PLAYER_SPEED
        if key_state[pg.K_a]:
            self.speed_x = -self.PLAYER_SPEED
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # Czas trwania bonusu (podwójny pocisk)
        if self.power and pg.time.get_ticks() - self.power_time > POWER_UP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()

    def shoot(self, game):
        """Metoda odpowiadająca za wystrzeliwanie pocisków przez gracza.

        Metoda sprawdza czy gracz zebrał bonus (podwójny pocisk) i generuje odpowiednią ilość pocisków.
        Metoda odpowiada także za uruchamianie dźwięków strzelania.

        Argumenty:
            game: obiekt klasy Game
        """
        if self.power == 0:
            bullet = Bullet(game, self.rect.centerx, self.rect.top)
            game.all_entities.add(bullet)
            game.bullets.add(bullet)
            game.laser_sound.play()
        if self.power == 1:
            bullet_1 = Bullet(game, self.rect.left, self.rect.centery)
            bullet_2 = Bullet(game, self.rect.right, self.rect.centery)
            game.all_entities.add(bullet_1, bullet_2)
            game.bullets.add(bullet_1, bullet_2)
            game.laser_sound.play()

    def power_up(self):
        """Metoda przyznająca zebrany przez gracza bonus (podwójny pocisk)."""
        self.power = 1
        self.power_time = pg.time.get_ticks()


class Enemy(pg.sprite.Sprite):
    """Klasa symulująca meteoryty."""

    ROTATION_RANGE = 8
    POSITION_Y_RANGE = -100
    SPEED_X_RANGE = 3
    SPEED_Y_RANGE = 9
    ROTATION_SMOOTHNESS = 30
    DISAPPEAR_TOLERANCE = 50

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(game.meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(self.POSITION_Y_RANGE, self.POSITION_Y_RANGE / 2.5)
        self.speed_x = random.randrange(-self.SPEED_X_RANGE, self.SPEED_X_RANGE)
        self.speed_y = random.randrange(self.SPEED_Y_RANGE / 9, self.SPEED_Y_RANGE)
        self.rotation = 0
        self.rotation_speed = random.randrange(-self.ROTATION_RANGE, self.ROTATION_RANGE)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        """Metoda odpowiadająca za rotację meteorytów."""
        now = pg.time.get_ticks()
        if now - self.last_update > self.ROTATION_SMOOTHNESS:
            self.last_update = now
            self.rotation += self.rotation_speed % 360
            new_image = pg.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        """Metoda odpowiada za poruszanie się meteorytów."""
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if (self.rect.top > HEIGHT + self.DISAPPEAR_TOLERANCE
                or self.rect.left < -self.DISAPPEAR_TOLERANCE
                or self.rect.right > WIDTH + self.DISAPPEAR_TOLERANCE):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(self.POSITION_Y_RANGE, self.POSITION_Y_RANGE / 2.5)
            self.speed_y = random.randrange(self.SPEED_Y_RANGE / 9, self.SPEED_Y_RANGE)


class Bullet(pg.sprite.Sprite):
    """Klasa symulująca pociski wystrzeliwane przez gracza."""

    BULLET_SPEED = 10

    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = game.bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -self.BULLET_SPEED

    def update(self):
        """Metoda odpowiada za poruszanie się pocisków oraz usuwanie ich gdy trafią poza okno gry."""
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pg.sprite.Sprite):
    """Klasa odpowiadająca za bonusy wypadające z zestrzelonych wrogów."""

    POWER_UP_SPEED = 6

    def __init__(self, game, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'laser'])
        self.image = game.powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = self.POWER_UP_SPEED

    def update(self):
        """Metoda odpowiadająca za opadanie bonusów oraz usuwanie ich, jeżeli trafią poza okno gry."""
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()


def main():
    game = Game()

    # Główna pętla gry

    while game.running:
        if game.game_over:
            game.game_start()

        # Określenie ilości klatek na sekundę

        game.clock.tick(FPS)

        # Obsługa zdarzeń

        game.events()

        # Aktualizacja stanu obiektów w grze

        game.all_entities.update()

        # Obsługa kolizji obiektów

        game.collision()

        # Funkcja rysująca obiekty na ekranie

        game.draw()

    pg.quit()
    quit()


if __name__ == '__main__':
    main()
