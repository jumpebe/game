# rain.py

import sys
import pygame
from raindrop import Raindrop


class Rain:
    """雨を描写。動作とアセットを管理する全体的なクラス"""

    def __init__(self):
        """初期化"""
        pygame.init()
        # 画面周りを設定
        self.screen = pygame.display.set_mode((0, 0),
                                              pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.bg_color = (0, 152, 203)
        pygame.display.set_caption("雨粒の描写")
        # 雨粒のインスタンスを作成
        self.raindrop = Raindrop(self)
        self.raindrops = pygame.sprite.Group()

        # 画面表示時の雨粒
        self.raindrop_spot()

    def run_game(self):
        """ゲームのループ処理"""
        while True:
            self.update_screen()
            self.raindrops.update()
            self.raindrops.draw(self.screen)
            self.undraw_raindrops()
            self.check_event()

            # 最新の状態に画面を描写
            pygame.display.flip()

    def raindrop_spot(self):
        """雨粒を格子状に配置するために雨粒の数を決める"""
        raindrop = Raindrop(self)
        raindrop_width, raidrop_height = raindrop.rect.size
        # 雨粒を配置する横幅のスペースを決定
        available_apace_x = self.screen_width - 2 * raindrop_width
        # １列に配置する雨粒の数
        number_raindriops = available_apace_x // (2 *
                                                  raindrop_width)
        # 雨粒を配置する縦方向の列を決める
        available_apace_y = self.screen_height // 3
        # 列数を決める
        row_raindrops = available_apace_y // (2 * raidrop_height)

        self.make_raindrop_row_line(number_raindriops, row_raindrops)

    def make_raindrop_row_line(self, number_raindriops, row_raindrops):
        """雨粒を配置する列と行を作成"""
        raindrop = Raindrop(self)
        raindrop_width, raidrop_height = raindrop.rect.size
        for raindrop_number in range(number_raindriops):
            for raindrop_row in range(row_raindrops):
                # 雨粒を作成して列に追加
                raindrop = Raindrop(self)
                raindrop.x = raindrop_width + (3 * raindrop_width
                                               * raindrop_number)
                raindrop.rect.x = raindrop.x
                raindrop.y = (raidrop_height +
                              (3 * raidrop_height * raindrop_row))
                raindrop.rect.y = raindrop.y
                self.raindrops.add(raindrop)

    def undraw_raindrops(self):
        """画面から消えた雨粒を消す。同時に雨を降らす"""
        # raindropのコピーでループを回す
        for raindrop in self.raindrops.copy():
            if raindrop.rect.top >= self.screen_height:
                self.raindrops.remove(raindrop)
                # 画面上部から再び雨を降らす
                new_raindrops = Raindrop(self)
                new_raindrops.rect.x = raindrop.rect.x
                self.raindrops.add(new_raindrops)

    def check_event(self):
        """イベントを管理するクラス"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update_screen(self):
        """画面を更新するモジュール"""
        self.screen.fill(self.bg_color)


if __name__ == "__main__":
    rn = Rain()
    rn.run_game()
