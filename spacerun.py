"""Projekt zaliczeniowy JS - Bartosz Knapik."""

import os
import random

import pygame as pg

import assets

# Stałe projektu.
TITLE = 'SPACE RUN'
HIGHSCORE_FILE = "highscores.dat"
WIDTH_PX = 800
HEIGHT_PX = 600
FPS = 60
POWER_UP_TIME_MS = 5000
BAR_LENGTH_PX = 180
BAR_HEIGHT_PX = 15
ENEMIES_NUMBER = 40
POWER_UP_CHANCE = 0.05  # Procentowa szansa na pojawienie się bonusu (*100%)
BG_SPEED = 4  # Szybkość przewijania tła gry

# Kolory
SURFACE_COLOR = pg.Color('#000000')
TEXT_COLOR_WHITE = pg.Color('#ffffff')
TEXT_COLOR_RED = pg.Color('#ac0103')
TEXT_COLOR_BLUE = pg.Color('#0579d4')
LIFE_BAR_COLOR = pg.Color('#3bcb4f')
POWER_UP_BAR_COLOR = pg.Color('#268bd2')
BAR_OUTLINE_COLOR = pg.Color('#e6e1e3')

# Ścieżki:
GAME_FOLDER = assets.GAME_FOLDER


class Game:
    """Główna klasa gry.

    Klasa inicjalizuje biblioteki, ładuje grafikę, czcionki i dźwięki używane w grze.
    Zawiera metody odpowiedzialne za rysowanie obiektów na ekranie (tekstu, grafiki).
    Obsługuje kolizję obiektów oraz koordynuje działanie gry.
    """
    # pylint: disable=too-many-instance-attributes, too-many-arguments, no-member

    SCREEN = pg.display.set_mode((WIDTH_PX, HEIGHT_PX))
    CLOCK = pg.time.Clock()

    def __init__(self, assts):
        self.assets = assts
        self.running = True
        self.game_over = True
        self.score = 0
        self.bg_y1 = 0
        self.bg_y2 = -HEIGHT_PX
        self.all_entities = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.power_up_time_ms = 0
        self.player = None

    def draw_text(self, font, pos, text, color, x_pos, y_pos):
        """Metoda odpowiedzialna za wyświetlanie tekstu w oknie gry.

        Argumenty:
            font: Czcionka, której ma użyć funkcja do wyświetlenia napisu.
            pos: Pozycja tekstu na ekranie.
            text: Tekst do wyświetlenia.
            color: Kolor tekstu.
            x_pos: Współrzędna "x" tekstu.
            y_pos: Współrzędna "y" tekstu.
        """

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if pos == 'midtop':
            text_rect.midtop = (x_pos, y_pos)
        else:
            text_rect.topleft = (x_pos, y_pos)
        self.SCREEN.blit(text_surface, text_rect)

    def show_menu(self):
        """Metoda odpowiedzialna za wyświetlanie ekranu startowego i
        wczytanie najlepszego wyniku."""

        self.SCREEN.blit(self.assets.background, self.assets.background_rect)
        self.draw_text(self.assets.title_font, 'midtop', TITLE, TEXT_COLOR_WHITE, WIDTH_PX / 2, HEIGHT_PX / 8)
        self.draw_text(self.assets.small_font, 'midtop', 'Press SPACE to play . . .',
                       TEXT_COLOR_BLUE, WIDTH_PX / 2, HEIGHT_PX / 3)
        self.draw_text(self.assets.small_font, 'midtop', 'SPACE - shoot',
                       TEXT_COLOR_RED, WIDTH_PX / 2, HEIGHT_PX / 2.2)
        self.draw_text(self.assets.small_font, 'midtop', 'A , D - move',
                       TEXT_COLOR_RED, WIDTH_PX / 2, HEIGHT_PX / 2)

        # Wczytanie najlepszego wyniku:
        with open(os.path.join(GAME_FOLDER, HIGHSCORE_FILE), 'r') as file:
            highscore = int(file.read())
        if self.score > highscore:
            self.draw_text(self.assets.medium_font, 'midtop', 'NEW HIGHSCORE:  '
                           + str(self.score), TEXT_COLOR_WHITE, WIDTH_PX / 2, HEIGHT_PX / 1.5)
            with open(os.path.join(GAME_FOLDER, HIGHSCORE_FILE), 'w') as file:
                file.write(str(self.score))
        else:
            self.draw_text(self.assets.medium_font, 'midtop', 'HIGHSCORE:  '
                           + str(highscore), TEXT_COLOR_WHITE, WIDTH_PX / 2, HEIGHT_PX / 1.5)

        pg.display.flip()
        waiting = True
        while waiting:
            self.CLOCK.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def draw_status_bar(self, x_pos, y_pos, color, value):
        """Metoda odpowiadająca za wyświetlanie się paska statusu naszego bonusu (podwójny pocisk).

        Argumenty:
            x_pos: Współrzędna "x" paska.
            y_pos: Współrzędna "y" paska.
            color: Kolor wypełnienia paska.
            value: Poziom wypełnienia paska.
        """

        if value < 0:
            value = 0
        fill = (value / 100) * BAR_LENGTH_PX
        outline_rect = pg.Rect(x_pos, y_pos, BAR_LENGTH_PX, BAR_HEIGHT_PX)
        fill_rect = pg.Rect(x_pos, y_pos, fill, BAR_HEIGHT_PX)
        pg.draw.rect(self.SCREEN, color, fill_rect)
        pg.draw.rect(self.SCREEN, BAR_OUTLINE_COLOR, outline_rect, 2)

    def spawn_enemy(self):
        """Metoda odpowiadająca za pojawianie się wrogów."""

        enemy = Enemy(self.assets)
        self.all_entities.add(enemy)
        self.enemies.add(enemy)

    def events(self):
        """Metoda obsługująca zdarzenia (strzelanie, wyjście z gry)."""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot()

    def clean_up(self):
        """Metoda usuwa wszystkie jednostki z planszy."""

        for entity in self.all_entities:
            entity.kill()

    def collision(self):
        """Metoda obsługująca kolizję obiektów w grze i
        wykonująca odpowiednie akcje, zależne od rodzaju kolizji."""

        hits = pg.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 1
            random.choice(self.assets.hit_sounds).play()
            if random.random() > 1 - POWER_UP_CHANCE:
                powerup = PowerUp(self.assets, hit.rect.center)
                self.all_entities.add(powerup)
                self.powerups.add(powerup)
            self.spawn_enemy()

        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        self.power_up_time_ms = 2 * (pg.time.get_ticks() - self.player.power_time) / 100
        for hit in hits:
            if hit.type == 'hp':
                self.assets.power_up_hp_sound.play()
                self.player.life += 20
                if self.player.life >= self.player.PLAYER_LIFE:
                    self.player.life = self.player.PLAYER_LIFE
            if hit.type == 'laser':
                self.assets.power_up_laser_sound.play()
                self.player.power_up()

        hits = pg.sprite.spritecollide(self.player, self.enemies, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.life -= hit.radius * 2
            self.spawn_enemy()
            if self.player.life <= 0:
                self.assets.death_sound.play()
                self.game_over = True
                self.clean_up()

    def draw(self):
        """Metoda odpowiada za ciągłe przewijanie tła gry oraz
        wyświetlanie punktów, paska stanu zdrowia i bonusu."""

        self.SCREEN.fill(SURFACE_COLOR)
        self.SCREEN.blit(self.assets.background, (0, self.bg_y1))
        self.SCREEN.blit(self.assets.background, (0, self.bg_y2))
        self.bg_y1 += BG_SPEED
        self.bg_y2 += BG_SPEED
        if self.bg_y1 > HEIGHT_PX:
            self.bg_y1 = 0
        if self.bg_y2 > 0:
            self.bg_y2 = -HEIGHT_PX

        self.all_entities.draw(self.SCREEN)
        self.draw_text(self.assets.small_font, 'midtop', 'score  '
                       + str(self.score), TEXT_COLOR_WHITE, WIDTH_PX / 2, 10)
        self.draw_text(self.assets.small_font, 'topleft', 'HP ', TEXT_COLOR_WHITE, 10, 10)
        self.draw_status_bar(50, 12, LIFE_BAR_COLOR, self.player.life)
        if self.player.power:
            self.draw_text(self.assets.small_font, 'topleft', 'UP ', TEXT_COLOR_WHITE, 10, 32)
            self.draw_status_bar(50, 32, POWER_UP_BAR_COLOR, (100 - self.power_up_time_ms))
        pg.display.flip()

    def game_start(self):
        """Metoda inicjująca grę.

        Metoda ustawia gracza oraz odpowiednią ilość wrogich obiektów w oknie gry.
        """

        self.show_menu()
        self.game_over = False
        self.player = Player(self, self.assets)
        self.all_entities.add(self.player)

        for i in range(ENEMIES_NUMBER):
            self.spawn_enemy()

        self.score = 0


class Player(pg.sprite.Sprite):
    """Klasa reprezentująca gracza."""
    # pylint: disable=too-many-instance-attributes

    PLAYER_SPEED = 15
    PLAYER_LIFE = 100

    def __init__(self, game, assts):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.assets = assts
        self.image = self.assets.player_img
        self.image.set_colorkey(SURFACE_COLOR)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH_PX / 2
        self.rect.bottom = HEIGHT_PX - 10
        self.speed_x = 0
        self.life = self.PLAYER_LIFE
        self.power = 0
        self.power_time = pg.time.get_ticks()

    def update(self):
        """Metoda odpowiadająca za poruszanie się gracza.

        Metoda umożliwia poruszanie się statku poprzez wykrywanie wciśniętego przycisku.
        Metoda zapobiega również wychodzeniu statku poza krawędzie okna gry.
        Metoda odpowiada także za wyłączenie bonusu podwójnego lasera po odpowiednim czasie.
        """
        # pylint: disable=no-member

        self.speed_x = 0
        key_state = pg.key.get_pressed()
        if key_state[pg.K_d]:
            self.speed_x = self.PLAYER_SPEED
        if key_state[pg.K_a]:
            self.speed_x = -self.PLAYER_SPEED
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH_PX:
            self.rect.right = WIDTH_PX
        if self.rect.left < 0:
            self.rect.left = 0

        # Czas trwania bonusu (podwójny pocisk)
        if self.power and pg.time.get_ticks() - self.power_time > POWER_UP_TIME_MS:
            self.power -= 1
            self.power_time = pg.time.get_ticks()

    def shoot(self):
        """Metoda odpowiadająca za wystrzeliwanie pocisków przez gracza.

        Metoda sprawdza czy gracz zebrał bonus (podwójny pocisk) i
        generuje odpowiednią ilość pocisków.
        Metoda odpowiada także za uruchamianie dźwięków strzelania.
        """

        if self.power == 0:
            bullet = Bullet(self.assets, self.rect.centerx, self.rect.top)
            self.game.all_entities.add(bullet)
            self.game.bullets.add(bullet)
            self.assets.laser_sound.play()
        if self.power == 1:
            bullet_1 = Bullet(self.assets, self.rect.left, self.rect.centery)
            bullet_2 = Bullet(self.assets, self.rect.right, self.rect.centery)
            self.game.all_entities.add(bullet_1, bullet_2)
            self.game.bullets.add(bullet_1, bullet_2)
            self.assets.laser_sound.play()

    def power_up(self):
        """Metoda przyznająca zebrany przez gracza bonus (podwójny pocisk)."""

        self.power = 1
        self.power_time = pg.time.get_ticks()


class Enemy(pg.sprite.Sprite):
    """Klasa symulująca meteoryty."""
    # pylint: disable=too-many-instance-attributes

    ROTATION_RANGE = 8
    POSITION_Y_RANGE = -100
    SPEED_X_RANGE = 3
    SPEED_Y_RANGE = 9
    ROTATION_SMOTHNESS = 30
    DISAPPEAR_TOLERANCE = 50

    def __init__(self, assts):
        pg.sprite.Sprite.__init__(self)
        self.assets = assts
        self.image_orig = random.choice(assts.meteor_images)
        self.image_orig.set_colorkey(SURFACE_COLOR)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        self.rect.x = random.randrange(WIDTH_PX - self.rect.width)
        self.rect.y = random.randrange(self.POSITION_Y_RANGE, self.POSITION_Y_RANGE / 2.5)
        self.speed_x = random.randrange(-self.SPEED_X_RANGE, self.SPEED_X_RANGE)
        self.speed_y = random.randrange(self.SPEED_Y_RANGE / 9, self.SPEED_Y_RANGE)
        self.rotation = 0
        self.rotation_speed = random.randrange(-self.ROTATION_RANGE, self.ROTATION_RANGE)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        """Metoda odpowiadająca za rotację meteorytów."""

        now = pg.time.get_ticks()

        if now - self.last_update > self.ROTATION_SMOTHNESS:
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
        if (self.rect.top > HEIGHT_PX + self.DISAPPEAR_TOLERANCE
                or self.rect.left < -self.DISAPPEAR_TOLERANCE
                or self.rect.right > WIDTH_PX + self.DISAPPEAR_TOLERANCE):
            self.rect.x = random.randrange(WIDTH_PX - self.rect.width)
            self.rect.y = random.randrange(self.POSITION_Y_RANGE, self.POSITION_Y_RANGE / 2.5)
            self.speed_y = random.randrange(self.SPEED_Y_RANGE / 9, self.SPEED_Y_RANGE)


class Bullet(pg.sprite.Sprite):
    """Klasa symulująca pociski wystrzeliwane przez gracza."""
    # pylint: disable=too-few-public-methods

    BULLET_SPEED = 10

    def __init__(self, assts, x_pos, y_pos):
        pg.sprite.Sprite.__init__(self)
        self.image = assts.bullet_img
        self.image.set_colorkey(SURFACE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.bottom = y_pos
        self.speed_y = -self.BULLET_SPEED

    def update(self):
        """Metoda odpowiada za poruszanie się pocisków oraz
        usuwanie ich gdy trafią poza okno gry."""

        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pg.sprite.Sprite):
    """Klasa odpowiadająca za bonusy wypadające z zestrzelonych wrogów."""
    # pylint: disable=too-few-public-methods

    POWER_UP_SPEED = 6

    def __init__(self, assts, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'laser'])
        self.image = assts.powerup_images[self.type]
        self.image.set_colorkey(SURFACE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = self.POWER_UP_SPEED

    def update(self):
        """Metoda odpowiadająca za opadanie bonusów oraz
        usuwanie ich, jeżeli trafią poza okno gry."""

        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT_PX:
            self.kill()


def main():
    """Główna funkcja projektu. Inicjalizuje zewnętrzne biblioteki.

    Mieści się w niej główna pętla gry odpowiadająca za jej prawidłowe działanie.
    """
    # pylint: disable=no-member

    # Inicjalizacja bibliotek
    pg.init()

    # Wczytanie zasobów z dysku
    assts = assets.Assets()
    assts.load()

    # Utworzenie obiektu klasy 'Game'
    game = Game(assts)
    pg.display.set_caption(TITLE)
    pg.display.set_icon(assts.icon)
    pg.mixer.music.play(loops=-1)

    # Główna pętla gry
    while game.running:
        if game.game_over:
            game.game_start()

        # Określenie ilości klatek na sekundę
        game.CLOCK.tick(FPS)
        # Obsługa zdarzeń
        game.events()
        # Aktualizacja stanu obiektów w grze
        game.all_entities.update()
        # Obsługa kolizji obiektów
        game.collision()
        # Funkcja rysująca obiekty na ekranie
        game.draw()

    pg.quit()


if __name__ == '__main__':
    main()
