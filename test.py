# from asyncore import close_all
import sys
# from zoneinfo import available_timezones
import pygame
from settings import Setting
from ship import Ship
from bullet import Bullet
from xyj import Xyj
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard

class daxlx:
    #waixingren
    """"外星人，管理游戏资源和行为的类"""
    def __init__(self):
        """"初始化游戏并创建游戏资源"""

        pygame.init()
        self.settings=Setting()

        #屏幕长宽
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("da xlx")

        # 创建存储游戏统计信息的实例，并创建记分牌
        self.stats=GameStats(self)
        self.sb = Scoreboard(self)

        #引入飞船
        self.ship=Ship(self)
        #定义储存子弹的编组
        self.bullets=pygame.sprite.Group()
        #定义洗衣机的编组
        self.xyjs=pygame.sprite.Group()
        self._create_fleet()

        #创建Play按钮
        self.play_button = Button(self,'Play')

        #设置背景色
        self.bg_color = (230,230,230)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_xyjs()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
            #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """单击PLAY开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏设置
            self.settings.initializa_dynamic_settings()

            #重置游戏统计信息
            self.stats.rest_stats()
            self.stats.game_active=True

            #重置计分牌图像
            self.sb.prep_score()
            # self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.xyjs.empty()
            self.bullets.empty()
            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            #隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹位置
        self.bullets.update()
        #检测洗衣机与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.xyjs):
            print("Ship hit!!!")
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        #检查是否有子弹击中了洗衣机
        #如果击中删除相应的子弹和洗衣机
        self._check_bullet_xyj_collisions()#collision碰撞，冲突

    def _check_bullet_xyj_collisions(self):
        """响应子弹与洗衣机碰撞"""
        #删除碰撞的子弹与洗衣机
        collisions=pygame.sprite.groupcollide(self.bullets,self.xyjs,True,True)
        if collisions:
            for xyjs in collisions.values():
                self.stats.score+=self.settings.xyj_points*len(xyjs)
            self.sb.prep_score()
                #一次循环中有两颗子弹射中了外星人，
                # 或者因子弹更宽而同时击中了多个外星人，
                # 玩家将只能得到一个被消灭的外星人的点数
            self._check_high_score()
        
        if len(self.xyjs)==0:
            #如果洗衣机全部消灭了，删除子弹并创建新的一群洗衣机
            self.bullets.empty()
            self.settings.increase_speed()
            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

            self._create_fleet()

    def _check_keydown_events(self,event):
        """响应按键"""
        if event.key==pygame.K_RIGHT:
            #向右移动
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            #向左移动
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            #按q结束关闭游戏
            sys.exit()      
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            #停止向右
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            #停止向左
            self.ship.moving_left=False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets)<self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_xyjs(self):
        """检查是否有洗衣机位于屏幕边缘，并更新洗衣机群的位置"""
        self._check_fleet_edges()
        self.xyjs.update()
        #检测洗衣机和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.xyjs):
            self._ship_hit()
        self._check_xyjs_bottom()

    def _check_xyjs_bottom(self):
        """检查是否有洗衣机到达屏幕底端"""
        screen_rect=self.screen.get_rect()
        for xyj in self.xyjs.sprites():
            if xyj.rect.bottom>=screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ship_left>0:
            #飞船减1
            self.stats.ship_left-=1
            #显示还有多少飞船
            self.sb.prep_ships()
            #清空子弹列表和洗衣机列表，并创建新的
            self.xyjs.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(2)
        else:
            self.stats.game_active=False
            #游戏结束，显示光标
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color) 
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.xyjs.draw(self.screen)

        self.sb.show_score()

        #如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        #让最近绘制的屏幕可见 
        pygame.display.flip()

    def _create_fleet(self):
        """创建洗衣机群"""
        number_xyj_y=self.get_number_rows()
        number_xyj_x=self.get_number_lines()
        #创建第一行洗衣机
        for xyj_number_y in range(number_xyj_y):
            for xyj_number in range(number_xyj_x):
                self._create_xyj(xyj_number,xyj_number_y)

    def get_number_lines(self):
        """计算屏幕可以显示多少列洗衣机"""
        xyj=Xyj(self)
        xyj_width=xyj.rect.width
        available_space_x=self.settings.screen_width-(xyj_width)
        number_xyj_x=available_space_x//int((2*xyj_width))
        return number_xyj_x 

    def get_number_rows(self):
        """计算屏幕可以显示多少行洗衣机"""
        xyj=Xyj(self)
        ship=Ship(self)
        xyj_height=xyj.rect.height
        available_xyj_y=self.settings.screen_height-3*xyj_height-ship.rect.height
        number_xyj_rows=available_xyj_y//int(2*xyj.rect.height)
        return number_xyj_rows

    def _create_xyj(self,xyj_number,xyj_rows):
        """创建一个洗衣机并将其放在当前行"""
        xyj=Xyj(self)
        xyj_width=xyj.rect.width
        xyj.x=int(0.35*xyj_width)+2*xyj_width*xyj_number
        xyj.rect.x=xyj.x
        xyj.rect.y=xyj.rect.height+1.5*xyj.rect.height*xyj_rows
        self.xyjs.add(xyj)

    def _check_fleet_edges(self):
        """有洗衣机达到边缘时采取对应措施"""
        for xyj in self.xyjs.sprites():
            if xyj.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """洗衣机群向下移动，并改变他们的方向"""
        for xyj in self.xyjs.sprites():
            xyj.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_high_score(self):
        """检查是否出现最高分"""
        if self.stats.score > self.stats.high_score: 
            self.stats.high_score = self.stats.score 
            self.sb.prep_high_score()

if __name__=='__main__':
    #创建游戏实例并运行
    ai=daxlx()
    ai.run_game()