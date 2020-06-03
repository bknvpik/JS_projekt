"""Testy modułu spacerun."""

import unittest

import pygame as pg

import assets
import spacerun


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.player = spacerun.Player(spacerun.Game(assts), assts)
        self.player.rect.right = 1000

    def test_update(self):
        self.player.update()
        self.assertEqual(self.player.rect.right, 800)


if __name__ == '__main__':
    pg.init()
    pg.font.init()
    pg.mixer.init()
    assts = assets.Assets()
    assts.load()
    unittest.main()
