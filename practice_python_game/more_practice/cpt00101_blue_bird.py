import sys

import pygame

class BlueBird:
    """青い背景のpygameウインドウを管理する"""
    
    def __init__(self):
        """初期化"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        self.bg_color = (135,206,250)
        
        pygame.display.set_caption("青い鳥")

    
    def run_game(self):
        """ゲームのループを回す"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.screen.fill(self.bg_color)
            pygame.display.flip()  
        
                    
if __name__ == "__main__":
    bb = BlueBird()
    bb.run_game()
        
    