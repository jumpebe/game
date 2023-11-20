import sys

import pygame

class George:
    """おサルのジョージを管理するクラス"""

    def __init__(self):
        """初期化と画面の基本情報作成"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.bg_color = (255, 255, 255)
        
        pygame.display.set_caption("おサルのジョージ")
        
        #画像を読み込み、サイズを取得
        self.image = pygame.image.load("image/george.bmp")
        self.rect = self.image.get_rect()
        self.center = self.screen.get_rect().center

        
    def run_game(self):
        """ゲームのループ"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.screen.fill(self.bg_color)
            self.screen.blit(self.image, self.center)
            pygame.display.flip()
            
                    
                    
if __name__ == "__main__":
    gg = George()
    gg.run_game()

        