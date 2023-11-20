import pygame


class Button:

    def __init__(self, ai_game, msg):
        """ボタン属性を初期化する"""
        self.screen = ai_game.screen
        self.sceen_rect = self.screen.get_rect()

        # ボタンの大きさと属性を設定する
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 46)

        # ボタンのrectオブジェクトを生成し、画面の中央に配置する
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.sceen_rect.center

        # ボタンのメッセージは一度だけ準備する必要がある
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """msgを画面に変換し、ボタンの中央に配置する"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """空白のボタンを描写し、msgを描写する"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
