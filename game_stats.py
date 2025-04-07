class GameStats:
    """控制游戏初始状态信息的类"""
    def __init__(self, ai_game):
        self.game_active = False
        self.ship_last = ai_game.settings.ship_limit
        self.high_score = 0
        self.score = 0
        self.level = 1
