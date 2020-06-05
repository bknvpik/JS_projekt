"""Testy modułu spacerun."""

import unittest

import pygame as pg

import assets
import spacerun


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.player = spacerun.Player(spacerun.Game(assts), assts)
        self.player.rect.right = 1000
        self.player.power = 0

    def test_update(self):
        self.player.update()
        self.assertEqual(self.player.rect.right, 800)
        self.player.rect.left = -100
        self.player.update()
        self.assertEqual(self.player.rect.left, 0)

    def test_power_up(self):
        self.player.power_up()
        self.assertTrue(self.player.power)

class BulletTest(unittest.TestCase):
    def setUp(self):
        self.player = spacerun.Player(spacerun.Game(assts), assts)
        self.game = spacerun.Game(assts)
        self.bullet = spacerun.Bullet(assts, self.player.rect.centerx, self.player.rect.top)
        self.game.bullets.add(self.bullet)
        self.bullet.rect.bottom = -100

    def test_update(self):
        self.bullet.update()
        self.assertEqual(len(self.game.bullets), 0)

class PowerUpTest(unittest.TestCase):
    def setUp(self):
        self.game = spacerun.Game(assts)
        self.power_up = spacerun.PowerUp(assts, (400, 50))
        self.game.powerups.add(self.power_up)
        self.power_up.rect.top = 700

    def test_update(self):
        self.power_up.update()
        self.assertEqual(len(self.game.powerups), 0)

if __name__ == '__main__':
    pg.init()

    assts = assets.Assets()
    assts.load()

    unittest.main()
