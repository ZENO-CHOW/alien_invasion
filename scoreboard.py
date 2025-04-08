import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ships = Group()

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 初始化当前得分板并设置坐标，放置在屏幕中央
        self.score_image = self.font.render(str(self.stats.score), True,
                                            self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.score_rect.top
        # 初始化最高得分板并设置坐标，放置在屏幕右侧
        self.high_score_image = self.font.render(str(self.stats.high_score), True,
                                                 self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = 20

        # 初始化等级显示，放置在历史最高分下
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.high_score_rect.right
        self.level_rect.top = self.high_score_rect.bottom + 10

        # 准备飞船图像
        self.prep_ships()

    def prep_score(self):
        # 显示当前得分
        round_score = round(self.stats.score, -1)  # 返回四舍五入后的分值
        score_str = "{:,}".format(round_score)  # 格式化数值，类似：100，000
        #创建一个文本并定义文本内容、文本颜色、文本背景填充
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

    def prep_high_score(self, high_score_value):
        # 得分
        high_score = round(high_score_value, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = 20

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

    def prep_ships(self):
        # 创建对应生命值个数的飞船并储存
        for ship_number in range(self.stats.ship_last):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        # 将分值、历史最高分值、等级、生命值绘制在屏幕上
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        # 检查分值是否超过历史最高分值
        if self.stats.score > self.stats.high_score:
            self.prep_high_score(self.stats.score)
