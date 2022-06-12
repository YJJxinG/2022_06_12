class Setting:
    """"存储游戏《打许鹭翔》中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800

        #背景颜色
        self.bg_color=(230,230,230)

        #飞船设置
        self.ship_speed=1.5
        self.ship_limit=3

        #子弹设置
        self.bullet_speed=1.5
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullet_allowed=3

        #外星人设置
        self.xyj_speed=1
        self.fleet_drop_speed=10
        #fleet_direction为1向右移动，-1表示向左移动
        self.fleet_direction=1

        # 以什么速度加快游戏节奏
        self.speedup_scale=1.1
        #随节奏增加的分数的速度
        self.score_scale=1.5

        #计分
        self.xyj_points=50

    def initializa_dynamic_settings(self):
        """初始化随游戏进行而改变"""
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.xyj_speed=1.0
        self.fleet_drop_speed=10
        #洗衣机移动方向
        self.fleet_direction=1

    def increase_speed(self):
        """提高游戏难度"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.xyj_speed *= self.speedup_scale
        self.fleet_drop_speed+=self.speedup_scale
        #增加得分
        self.xyj_points=int(self.xyj_points*self.score_scale)
        print(self.xyj_points)