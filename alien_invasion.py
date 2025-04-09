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
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # 实例化外星人舰队群
        self._create_fleet()
        # 实例化按键区域
        self.play_button = Button(self, "play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()  # 飞船位置更新函数
                self._update_bullets()  # 子弹
                self._update_alien()
            self._update_screen()  # 每次循环时都重新绘制屏幕

    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # 结束程序
            elif event.type == pygame.KEYDOWN:  # 检测键盘按键按下
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 检测键盘按键抬起
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 抓取鼠标点按动作
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        # 生成一个新的子弹并保证子弹数量不超过允许值
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        # 当鼠标点击按键区域时返回True
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 激活游戏状态
            self.stats.game_active = True
            # 清空并创建新的外新人舰队
            self.aliens.empty()
            self._create_fleet()
            # 清空子弹
            self.bullets.empty()
            pygame.mouse.set_visible(False)
            # 初始化游戏动态设定
            self.settings.initialize_dynamic_settings()
            self.stats.score = 0
            self.stats.level = 1
            # 重置积分板数值
            self.scoreboard_vision.prep_score()
            self.scoreboard_vision.prep_level()
            self.scoreboard_vision.prep_ships()
            # 重置飞船位置至初始状态
            self.ship.center_ship()

    def _update_bullets(self):
        self.bullets.update()  # 更新容器内所有子弹的位置
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                # 当子弹移动至屏幕外时，移除该子弹
                self.bullets.remove(bullet)
        self._check_bullets_alien_collisions()

    def _check_bullets_alien_collisions(self):
        # 检查子弹与外星人碰撞，参数True和True表示碰撞后会删除相应的精灵
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens, True, True)
        # pygame.sprite.groupcollide()返回一个字典，键为bullet，值为一个包含多个alien的列表，表示一个bullet与对应的alien碰撞
        if collisions:
            # 如果存在碰撞
            for aliens in collisions.values():
                # 使ailens遍历每一个包含存在碰撞的alien列表
                self.stats.score += self.settings.alien_points * len(aliens)
                self.scoreboard_vision.prep_score()
                self.scoreboard_vision.check_high_score()
        if not self.aliens:
            # 外星人清空时，升级到下一等级
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard_vision.prep_level()

    def _update_alien(self):
        # 更新外星人位置
        self._check_fleet_edge()  # 检测舰队边界
        self.aliens.update()  # 更新所有外星人的位置
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        # 检测外星人舰队底部是否到达游戏框底部
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 当外星人底部超出游戏框，游戏重新开始或彻底结束
                self._ship_hit()
                for alien_y in self.aliens.sprites():
                    # 将所有剩余的alien向上移动一定距离
                    alien_y.rect.y -= (2 * alien_y.rect.height + self.ship.rect.height)
                break

    def _check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # 如果为true，则改变舰队水平移动方向
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # 舰队向下移动一次并改变舰队移动方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

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

    def _ship_hit(self):
        # 当发生碰撞时，检测生命值后重新生成游戏
        if self.stats.ship_last > 0:
            self.stats.ship_last -= 1
            self.scoreboard_vision.prep_ships()
            # self.aliens.empty()  # 碰撞后清空并重新生成外星人
            # self._create_fleet()
            self.bullets.empty()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创建外星人群"""
        new_alien = Alien(self)
        new_alien_width, new_alien_height = new_alien.rect.size
        available_space_x = self.settings.screen_width - 2 * new_alien_width
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 3 * new_alien_height - ship_height
        number_alien_columns = available_space_x // (2 * new_alien_width)  # //为取整除法
        number_alien_rows = available_space_y // (2 * new_alien_height)
        for rows_number in range(number_alien_rows+1):
            for columns_number in range(number_alien_columns+1):
                self._create_new_alien(columns_number, rows_number, new_alien_width, new_alien_height)

    def _create_new_alien(self, columns_number, rows_number, new_alien_width, new_alien_height):
        # 创建一个外星人并指定相应的坐标
        new_alien = Alien(self)
        new_alien.x = new_alien_width + 2 * new_alien_width * columns_number
        new_alien.y = new_alien_height + 2 * new_alien_height * rows_number
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        # 将新建的外星人放入容器
        self.aliens.add(new_alien)


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
