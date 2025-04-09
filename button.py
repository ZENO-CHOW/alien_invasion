import pygame.font


# 定义一个按键类
class Button:
    """设置按键区域及区域内文本的类"""
    def __init__(self, ai_game, msg):  # msg=massage
        # 获取alien_invasion游戏窗口和窗口的位置
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # 实例化一个区域并设置区域大小作为按键
        self.width, self.height = 200, 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 设置将作为按键区域的位置
        self.rect.center = self.screen_rect.center
        # 定义两个变量，其储存颜色信息
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # 设置文字样式及大小
        self.font = pygame.font.SysFont(None, 48)
        # 创建文本并设置文本的内容、颜色、背景颜色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # 获取文本的外接矩形框
        self.msg_image_rect = self.msg_image.get_rect()
        # 设置文本的位置
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 在alien_invasion窗口上的指定区域填充指定颜色
        self.screen.fill(self.button_color, self.rect)
        # 将文本放置在alien_invasion窗口上
        self.screen.blit(self.msg_image, self.msg_image_rect)
