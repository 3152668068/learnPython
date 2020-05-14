import sys
import pygame
import random
gameScore=0

#设置游戏难度，参数为上下管道间隔
gameLevel={'easy':200,'normal':150,'hard':100}
#上下管道的位置
up=random.randint(-380,0)
down=random.randint(420+up+gameLevel['easy'],630)

#鸟类
class bird:

    def __init__(self):
        self.birdRect=pygame.Rect(65,50,50,50)
        self.img=pygame.image.load("img/bird.png")
        self.status=0
        self.birdX=100
        self.birdY=300
        self.jump=False
        self.jumpSpeed=10
        self.gravity=5
        self.dead=False
    #鸟类坐标位置的更新
    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed-=1
            self.birdY-=self.jumpSpeed
        else:
            self.gravity+=0.2
            self.birdY+=self.gravity
        self.birdRect[1]=self.birdY

#管道类
class pipeline:

    def __init__(self):
        self.wallx=400
        self.pineUp=pygame.image.load("img/up.png")
        self.pineDown = pygame.image.load("img/down.png")
    #更新管道类
    def updatePipeline(self):
        self.wallx-=5
        if self.wallx<-58:
            self.wallx=348
            global up, down,gameScore
            #随机数重置管道显示位置,跟据得分设置难度级别
            if gameScore<10:
                level=gameLevel['easy']
            elif gameScore<20:
                level=gameLevel['normal']
            else:
                level=gameLevel['hard']
            up = random.randint(-380, 0)
            down = random.randint(420 + up + level, 630)
            #得分+1
            gameScore+=1

#地图（鸟，管道，背景）绘制
def createMap():
    #背景
    screen.fill((255,255,255))
    screen.blit(background,(0,0))
    #鸟
    screen.blit(abird.img,(abird.birdX,abird.birdY))
    abird.birdUpdate()
    #管道
    screen.blit(pipelines.pineUp,(pipelines.wallx,up))  #-380-0
    screen.blit(pipelines.pineDown, (pipelines.wallx, down))  # 200-560
    pipelines.updatePipeline()
    #得分显示
    score = font.render('得分:%d' % gameScore, False, (255, 255, 255))
    screen.blit(score, (5, 5))

#检查游戏是否结束
def checkDead():
    #获取上下管道的Rect类
    upRect=pygame.Rect(pipelines.wallx,up-20,pipelines.pineUp.get_width()-10,pipelines.pineUp.get_height())
    downRect=pygame.Rect(pipelines.wallx,down+20,pipelines.pineDown.get_width()-10,pipelines.pineDown.get_height())
    #利用colliderect()方法判断是否和鸟的Rect重叠
    if upRect.colliderect(abird.birdRect) or downRect.colliderect(abird.birdRect):
        abird.dead=True
        return True
    #判断鸟是否掉出屏幕
    if not 0<abird.birdRect[1]<height:
        abird.dead=True
        return True
    else:
        return False

#显示游戏结果
def getResutl():
    #设置文字
    fontOne = pygame.font.SysFont("SimHei",20,True)
    text1=fontOne.render('游戏结束',False,(255,127,36))
    text2=fontOne.render('最终得分:%d'%gameScore,False,(255,127,36))
    text3=fontOne.render('按空格键返回主菜单',False,(255,127,36))
    #显示文字
    screen.blit(text1,(140,240))
    screen.blit(text2, (131, 280))
    screen.blit(text3, (85, 320))

#主程序
if __name__=='__main__':
    #初始化
    pygame.init()
    pygame.display.set_caption("Flppy Bird")
    #判断游戏是否开始
    gameStatus=0
    #设置宽高
    size=width,height=400,600
    screen=pygame.display.set_mode(size)
    #设置游戏帧数
    FpsClock=pygame.time.Clock()
    #初始化鸟，管道
    abird=bird()
    pipelines=pipeline()
    #初始化主菜单图片
    background=pygame.image.load('img/sky.png')
    titleImg=pygame.image.load('img/title.png')
    #设置游戏字体
    font = pygame.font.SysFont("SimHei", 20,True)
    #主循环
    while True:
        #设置游戏帧数
        FpsClock.tick(60)
        #判断游戏是否开始（主菜单）
        if not gameStatus:
            #绘制内容
            content = font.render('按任意键开始游戏', False, (255, 200, 10))
            screen.blit(background, (0, 0))
            screen.blit(titleImg, (0, 50))
            screen.blit(content, (120, 300))

            #监听是否开始游戏
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN):
                    gameStatus=1
                elif event.type==pygame.QUIT:
                    sys.exit(0)

        #游戏开始
        if gameStatus:
            # 检查游戏是否结束
            if checkDead():
                getResutl()
            else:
                createMap()
            for event in pygame.event.get():  # 事件监听
                if event.type == pygame.QUIT:
                    sys.exit(0)
                #控制鸟的上升
                if not abird.dead and ((event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN)):
                    abird.jump = True
                    abird.gravity = 5
                    abird.jumpSpeed = 10
                #如果游戏结束，按空格键重置游戏
                if abird.dead and ((event.type == pygame.KEYDOWN)):
                    gameStatus = 0
                    abird.dead = False
                    gameScore = 0
                    abird = bird()
                    pipelines = pipeline()
                    break

        #更新
        pygame.display.flip()
    #程序结束
    pygame.quit()





