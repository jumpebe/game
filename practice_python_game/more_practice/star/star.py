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
        self.bg_color = (200, 200, 200)
        pygame.display.set_caption("星")
        #画像の読み込みとサイズの取得
        self.image = pygame.image.load("image/star.bmp")
        self.image_rect = self.image.get_rect()
        #固定された星の座標
        self.star_coords = []
        for i in range(11):
            x = randint(0, self.screen_width)
            y = randint(0, self.screen_height)
            space = (x, y)
            self.star_coords.append(space)
     
    def check_event(self):
        """イベントを監視""" 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    def interspace_star(self):
        """星の位置をランダムに変える"""
        # for i in range(11):
        #     x = randint(0, self.screen_width)
        #     y = randint(0, self.screen_height)
        #     space = (x, y)
        #     self.screen.blit(self.image, space)
        for coord in self.star_coords:
            self.screen.blit(self.image, coord)
                 
    def update_screen(self):
        """画面を更新"""
        self.screen.fill(self.bg_color)
        self.interspace_star()
        pygame.display.flip()
        
    def run_game(self):
        """ゲームのループ"""
        self.check_event()
        self.update_screen()

if __name__ == "__main__":
    st = Star()
    while True:
        st.run_game()