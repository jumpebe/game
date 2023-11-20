# raindrop.py

import pygame
from pygame.sprite import Sprite


class Raindrop(Sprite):
    """雨粒を管理するクラス"""

    def __init__(self, rn_game):
        """雨粒を初期化して、開始時の位置を決定"""
        super().__init__()
        self.screen = rn_game.screen
        self.screen_rect = self.screen.get_rect()
        # 画像をロードして、サイズを取得
        self.image = pygame.image.load("0037_R_450.png")
        self.rect = self.image.get_rect()

        # 雨粒を画面上部に配置
        self.rect.top = 0

        # 雨粒のy軸を取得して、不動小数点で扱えるようにする
        self.y = float(self.rect.y)
        # 雨粒が下に落ちるスピード
        self.raindrop_speed = 1.0

    def update(self):
        """雨粒が画面下に落ちるモジュール"""
        self.y += self.raindrop_speed
        self.rect.y = self.y

    def blitme(self):
        """雨粒を画面に出力"""
        self.screen.blit(self.image, self.rect)
