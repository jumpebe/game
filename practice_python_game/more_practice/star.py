import sys

import pygame
from random import randint


class Star:
    """星を描写するクラス"""
    
    def __init__(self):
        """星を描写するクラスの初期化"""
        pygame.init()
        #画面の色と大きさに関する記述
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        self.bg_color = (230, 230, 230)
        pygame.display.set_caption("星")
        #画像の読み込みとサイズの取得
        self.image = pygame.image.load("image/star.bmp")
        self.image_rect = self.image.get_rect()

    def run_game(self):
        """画面のループ。イベント検知とアクション"""
        self.make_stardust()

    def make_stardust(self):
        """星を描写する処理をループするクラス"""
        while 10:
            x = randint(0, self.screen_width)
            y = randint(0, self.screen_height)
            space = (x, y)
            self.screen.blit(self.image, space)
        self.screen.fill(self.bg_color)
        pygame.display.flip()
  
        
    def check_event(self):
        """イベント管理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    st = Star()
    st.run_game()