import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """宇宙船から発射される弾を管理するクラス"""
    
    def __init__(self, ai_game):
        """宇宙船の現在位置から弾のオブジェクトを生成する"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        #弾のrectを(0,0)の位置に作成してから、正しい位置を設定する  
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midright = ai_game.ship.rect.midright
        
        #弾の位置を不動少数点で保存する
        self.x = float(self.rect.x)
        
    def update(self):
        """画面上の弾を移動する"""
        #弾の浮動小数点の位置を更新する
        self.x += self.settings.bullet_speed
        #rectの位置を更新する
        self.rect.x = self.x
        
    def draw_bullet(self):
        """画面上の弾を描写する"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    