# alien_invaision_horizontal.py
import sys
from time import sleep

import pygame
from settings_horizontal import Settings
from game_stats_horizontal import GameStats
from ship_horizontal import Ship
from alien_horizontal import Alien
from bullet_horizontal import Bullet


import random


class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        """ゲームを初期化し、ゲームのリソースを作成する"""
        pygame.init()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((
        #     self.settings.screen_width, self.settcdings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("エイリアン侵略")

        # ゲームの統計情報を格納するインスタンスを生成
        self.stats = GameStats(self)

        # 船のインスタンス作成
        self.ship = Ship(self)
        # スプライトのグループ作成
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # 開始時のエイリアンの描写
        self._create_fleet()

    def run_game(self):
        """ゲームのメインループを作成する"""
        while True:
            self._check_events()
            if self.stats.ships_left > 0:

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
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        self._check_collision_bullets_alians_collision()

    def _check_collision_bullets_alians_collision(self):
        """弾とエイリアンの衝突に対応する"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # エイリアンの数が15体より少なくなったら、エイリアンを生成する
        if len(self.aliens) <= 15:
            for _ in range(random.randint(1, 10)):
                self._add_alien()

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
            self.ship.midleft_ship()

            # いったん停止する
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _add_alien(self):
        """不足したエイリアンをランダムに生成"""
        alien = Alien(self)
        alien.rect.x = random.randint(
            self.settings.screen_width // 2,
            self.settings.screen_width)
        alien.rect.y = random.randint(
            self.settings.screen_height // 2,
            self.settings.screen_height)
        self.aliens.add(alien)

    def _create_fleet(self):
        """エイリアンの艦隊をつくる"""
        # エイリアンの配置場所と配置数を決める為のインスタンス
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        # 右半分の範囲でエイリアンを配置する
        available_space_x = (self.settings.screen_width -
                             self.settings.screen_width // 2)
        number_alien_x = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height
        number_alien_y = available_space_y // (alien_height * 2)
        self._create_alien(number_alien_x, number_alien_y,
                           available_space_x)

    def _create_alien(self, number_alien_x, number_alien_y,
                      available_space_x):
        """エイリアン軍隊の作成"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        # 楯列と横業のループを回す
        for alien_number in range(number_alien_x):
            for alien_line in range(number_alien_y):
                # x軸とy軸でそれぞれのエイリアンの位置を指定
                alien = Alien(self)
                alien.x = available_space_x + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.y = alien_height + alien_height * 1.5 * alien_line
                alien.rect.y = alien.y
                self.aliens.add(alien)

    def _check_fleet_edges(self):
        """エイリアンが画面の上下端にいるかどうかを確認"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """エイリアンの移動方向を変える"""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """エイリアン艦隊を動かす"""
        self._check_fleet_edges()
        self.aliens.update()

        # エイリアンと宇宙船の衝突を探す
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # エイリアンが画面一番左に到達したか探す
        self._check_aliens_left()

    def _check_aliens_left(self):
        """エイリアンが画面で左に到達したか確認する"""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._ship_hit()
                break

    def _update_screen(self):
        # ループする度に画面を再描写する
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # 最初の画面の状態を表示する
        pygame.display.flip()


if __name__ == "__main__":
    # ゲームのインスタンスを作成し実行
    ai = AlienInvasion()
    ai.run_game()
