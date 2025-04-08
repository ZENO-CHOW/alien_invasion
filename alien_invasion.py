import sys
import pygame
from time import sleep
# 自建文件
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        self.settings = Settings()
        pygame.init()
        # 实例化游戏窗口
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 设置窗口名称为"Alien Invasion"
        pygame.display.set_caption("Alien Invasion")
        # 设置游戏运行最初始的状态
        self.stats = GameStats(self)
        # 实例化计分板
        self.scoreboard_vision = Scoreboard(self)
        # 实例化飞船
        self.ship = Ship(self)   # ai.game=self=AlienInvasion(),此时ai.game成为一个实例对象
        # 创建两个容纳sprite的容器
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # 实例化外星人舰队群
        self._create_fleet()
        # 实例化按键区域
        self.play_button = Button(self, "play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()
            self._update_screen()  # 每次循环时都重新绘制屏幕

    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 抓取鼠标点按动作
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # 当鼠标点击按键区域时返回True
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            self.scoreboard_vision.prep_score()
            self.scoreboard_vision.prep_level()
            self.scoreboard_vision.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _update_screen(self):
        # 每次循环时都重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.location()
        # 让最近绘制的屏幕可见
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard_vision.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullets_alien_collisions()

    def _check_bullets_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.scoreboard_vision.prep_score()
                self.scoreboard_vision.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard_vision.prep_level()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星人群"""
        new_alien = Alien(self)
        new_alien_width, new_alien_height = new_alien.rect.size
        available_space_x = self.settings.screen_width - 2 * new_alien_width
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 3 * new_alien_height - ship_height
        number_alien_columns = available_space_x // (2 * new_alien_width)  # //为取整除法
        number_alien_rows = available_space_y // (2 * new_alien_height)
        for row_number in range(number_alien_rows+1):
            for alien_number in range(number_alien_columns+1):
                self._create_new_alien(alien_number, row_number, new_alien_width, new_alien_height)

    def _create_new_alien(self, alien_number, number_rows, new_alien_width, new_alien_height):
        # 创建一个外星人
        new_alien = Alien(self)
        new_alien.x = new_alien_width + 2 * new_alien_width * alien_number
        new_alien.y = new_alien_height + 2 * new_alien_height * number_rows
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien)

    def _update_alien(self):
        self._check_fleet_edge()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ship_last > 0:
            self.stats.ship_last -= 1
            self.scoreboard_vision.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
