import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        # 加载飞船图像并获取其外接矩形。
        self.image = pygame.image.load('images/fly_ship.bmp')
        self.rect = self.image.get_rect()
        # 对于每艘新飞船，都将其放在屏幕底部的中央。
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def location(self):
        """在指定位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 检测飞船移动情况并保证其不跑出游戏窗口外
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def center_ship(self):
        # 重置飞船位置在窗口底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
