import pygame.font

# 创建一个按钮，并定义其功能
class Button:
    def __init__(self, ai_game, msg):  # msg=massage
        # 获取alien_invasion游戏窗口和窗口的位置
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # 实例化一个按键
        self.width, self.height = 200, 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 设置按键位置
        self.rect.center = self.screen_rect.center
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # 设置文字大小
        self.font = pygame.font.SysFont(None, 48)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # 创建文本，设置文字内容、颜色，按键背景颜色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # 获取文本的位置
        self.msg_image_rect = self.msg_image.get_rect()
        # 设置文本的位置
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 将按键放置在alien_invasion窗口上
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
