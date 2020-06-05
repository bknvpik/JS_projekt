"""Zasoby potrzebne do działania gry."""

import os

import pygame as pg

# Rozmiary czcionek
SMALL_FONT_SIZE_PX = 20
MEDIUM_FONT_SIZE_PX = 30
TITLE_FONT_SIZE_PX = 80

# Ścieżki:
GAME_FOLDER = os.path.dirname(__file__)
IMG_FOLDER = os.path.join(GAME_FOLDER, 'img')
FONTS_FOLDER = os.path.join(GAME_FOLDER, 'fonts')
SOUNDS_FOLDER = os.path.join(GAME_FOLDER, 'sounds')


class Assets:
    """Klasa przechowuje zasoby."""
    # pylint: disable=too-few-public-methods

    @staticmethod
    def load():
        """Metoda wczytuje zasoby z dysku."""

        # Wczytanie plików graficznych
        Assets.icon = pg.image.load(os.path.join(IMG_FOLDER, 'icon.png'))
        Assets.menu_bg = pg.image.load(os.path.join(IMG_FOLDER, 'menu_bg.png')).convert()
        Assets.menu_bg_rect = Assets.menu_bg.get_rect()
        Assets.background = pg.image.load(os.path.join(IMG_FOLDER, 'background.png')).convert()
        Assets.background_rect = Assets.background.get_rect()
        Assets.player_img = pg.image.load(os.path.join(IMG_FOLDER, 'player.png')).convert()
        Assets.bullet_img = pg.image.load(os.path.join(IMG_FOLDER, 'laser.png')).convert()
        Assets.meteor_images = []
        meteor_list = ['meteorite_small.png', 'meteorite_medium.png', 'meteorite_big.png']
        for img in meteor_list:
            Assets.meteor_images.append(pg.image.load(os.path.join(IMG_FOLDER, img)).convert())
        Assets.powerup_images = dict()
        Assets.powerup_images['hp'] = pg.image.load(os.path.join(IMG_FOLDER, 'powerup_hp.png')).convert()
        Assets.powerup_images['laser'] = pg.image.load(os.path.join(IMG_FOLDER, 'powerup_laser.png')).convert()

        # Wczytanie czcionek
        Assets.small_font = pg.font.Font(os.path.join(FONTS_FOLDER, 'sterilict.ttf'), SMALL_FONT_SIZE_PX)
        Assets.medium_font = pg.font.Font(os.path.join(FONTS_FOLDER, 'sterilict.ttf'), MEDIUM_FONT_SIZE_PX)
        Assets.title_font = pg.font.Font(os.path.join(FONTS_FOLDER, 'dustifine.ttf'), TITLE_FONT_SIZE_PX)

        # Wczytanie dźwięków
        Assets.laser_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'laser.wav'))
        Assets.power_up_hp_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'powerup_hp.wav'))
        Assets.power_up_laser_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'powerup_laser.wav'))
        Assets.death_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'death.wav'))
        Assets.hit_sounds = []
        for snd in ['hit1.wav', 'hit2.wav']:
            Assets.hit_sounds.append(pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, snd)))
        pg.mixer.music.load(os.path.join(SOUNDS_FOLDER, 'soundtrack.mp3'))
