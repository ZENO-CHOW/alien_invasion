class Settings:
    """储存游戏初始化时所需设置信息的类"""
    def __init__(self):
        # 游戏窗口大小
        self.screen_width = 1200
        self.screen_height = 800
        # 设置游戏背景颜色
        self.bg_color = (230, 230, 230)
        # 飞船移动速度
        self.ship_speed = 0.5
        # 子弹的飞行速度、尺寸、颜色信息及同一时间下子弹的最大数量
        self.bullet_speed = 0.2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # 外星人移动速度
        self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1表示右移，-1表示左移
        # 飞船生命值
        self.ship_limit = 3
        # 速度（难度）增加系数
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.alien_points = 50
        # self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 0.5
        self.bullet_speed = 0.2
        self.alien_speed = 0.1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
