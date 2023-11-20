import sys
from time import sleep

import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        """ゲームを初期化し、ゲームのリソースを作成する"""
        pygame.init()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((
        #     self.settings.screen_width, self.settcdings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("エイリアン侵略")

        # ゲームの統計情報を格納するインスタンスを生成
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # playボタンを作成する
        self.play_button = Button(self, "Play")

    def run_game(self):
        """ゲームのメインループを作成する"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """キーボードとマウスのイベントを監視"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """プレイヤーが「Play」ボタンを押したらゲーム開始"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # ゲームの統計情報をリセットする
            self.stats.reset_stats()
            self.stats.game_active = True

            # 残ったエイリアンと弾を破棄する
            self.aliens.empty()
            self.bullets.empty()

            # 新しい艦隊を作成し、宇宙船を画面中央に配置する
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_event(self, event):
        """ボタンを押すイベントに:対応"""
        if event.key == pygame.K_RIGHT:
            # 宇宙船を右に移動する
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_event(self, event):
        """キーを離すイベントに対応"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _ship_hit(self):
        """エイリアンと宇宙船の衝突に対応する"""
        if self.stats.ships_left > 0:
            # 残りの宇宙船の数を減らす
            self.stats.ships_left -= 1
            # 残っていたエイリアンと弾を破棄する
            self.aliens.empty()
            self.bullets.empty()
            # 新しい艦隊を作成し、宇宙船を中央に配置する
            self._create_fleet()
            self.ship.center_ship()

            # いったん停止する
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _fire_bullet(self):
        """新しい弾を生成し、bulletグループに追加する"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """弾の位置を更新し、古い弾を廃棄する"""
        # 弾の位置を更新する
        self.bullets.update()

        # 見えなくなった弾を廃棄する
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collidion()

    def _check_bullet_alien_collidion(self):
        """弾とエイリアンが当たったかを調べる"""
        # その場合、対象の弾とエイリアンを廃棄する
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            # 存在する弾を破棄し、新しい艦隊を作成する
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        艦隊が画面の端にいるか確認してから
        艦隊にいる全エイリアンの位置を更新する
        """
        self._check_fleet_edges()
        self.aliens.update()

        # エイリアンと宇宙船の衝突を探す
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 画面の一番下に到達したエイリアンを探す
        self._check_aliens_bottom()

    def _create_fleet(self):
        """エイリアンの艦隊を作成する"""
        # 一匹のエイリアンを作成し、一列のエイリアンの数を求める
        # 各エイリアンの間にはエイリアン一匹分のスペースを空ける
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width * 2)
        number_aliens_x = available_space_x // (alien_width * 2)

        # 画面の見えるエイリアンの列を決定する
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (alien_height * 3) - ship_height)
        numer_rows = available_space_y // (2 * alien_height)

        for row_number in range(numer_rows):
            for alien_number in range(number_aliens_x):
                self._create_aliens(alien_number, row_number)

    def _create_aliens(self, alien_number, row_number):
        """エイリアンを一匹作成し列の中に配置する"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """エイリアンが画面の端に達した場合に適切な処理を行う"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """艦隊を下に移動し、横移動の方向を変更する"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """エイリアンが画面の一番下に到達したか確認する"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 宇宙船を破壊したときと同じように扱う
                self._ship_hit()
                break

    def _update_screen(self):
        # ループする度に画面を再描写する
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # ゲームが非アクティブな状態の時に「Play」ボタンを描写する
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 最初の画面の状態を表示する
        pygame.display.flip()


if __name__ == "__main__":
    # ゲームのインスタンスを作成し実行
    ai = AlienInvasion()
    ai.run_game()
