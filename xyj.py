import pygame
from pygame.sprite import Sprite

class Xyj(Sprite):
    """表示单个洗衣机的类"""

    def __init__(self,ai_game):
        """初始化洗衣机并设置起始位置"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        #加载外星人图像并设置其rect属性
        self.image=pygame.image.load('xyj_head2.bmp')
        self.rect=self.image.get_rect()

        #每个洗衣机最初都在屏幕左上角附近
        self.rect.x=self.rect.width
        self.rect.x=self.rect.height

        #储存洗衣机的精准水平位置
        self.x=float(self.rect.x)

    def check_edges(self):
        """如果洗衣机位移屏幕边缘，返回True"""
        screen_rect=self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            # print(screen_rect.right)
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """外星人的移动"""
        self.x += (self.settings.xyj_speed*self.settings.fleet_direction)
        self.rect.x=self.x