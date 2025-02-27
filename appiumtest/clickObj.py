import time


class clickObj:
    def __init__(self, x,y,desc,slp=1,duration=200, isOffset = False):
        self.x = x
        self.y = y
        self.desc = desc
        self.slp = slp
        self.duration = duration
        self.isOffset = isOffset
    def getLoc(self):
        if self.isOffset:
            return [(self.x,self.y)]
        return [(self.x,self.y),(self.x+10,self.y+10)]

    def click(self, driver):
        driver.tap(self.getLoc(), self.duration)
        print('******', self.desc, '点击了')
        time.sleep(self.slp)



unitSelector = clickObj(550, 1000, '进入关卡选择')
unitLeft = clickObj(60,960,'关卡选择左', 0.2)
unitRight = clickObj(1030,960,'关卡选择左', 0.2)
unitBack = clickObj(230, 1835, '关卡选择返回', 0.5)

startGameBtn = clickObj(550,1510, '开始游戏', 0.5)
startGameBtn1 = clickObj(420, 1200, '扫荡的开始游戏', 5)
getAllBtn = clickObj(530,1540, '获取全部秘宝', 0.8)
skipBtn = clickObj(995,80, '跳过广告btn', 0.5)

beisuBtn = clickObj(1000,80, '倍速按钮', 0.3, 100, True)

mijuanBtn = clickObj(550, 1380, '密卷确认', 0.3)

jinengBtn1 = clickObj(950, 1580, '技能1', 0.2)
jinengBtn2 = clickObj(950, 1400, '技能2', 0.2)

refreshMb = clickObj(540, 1400, '免费刷新', 0.2)
confirmMb = clickObj(540,1480, '确认秘宝', 0.2)

getPriceBtn = clickObj(550, 1720,'领取奖励', 5)

homeBtn1 = clickObj(550,1830, '主页按钮1',0.3)
homeBtn2 = clickObj(520,1830, '主页按钮2',0.3)

cityBtn = clickObj(960, 1830, '城镇按钮1', 0.5)

houseBtn = clickObj(200,1000, '勇者小屋', 0.3)

diaoBtn = clickObj(400,1500,'进入钓鱼', 0.5)
startFishBtn = clickObj(500, 1600, '开始钓鱼', 5)
sellBtn = clickObj(420, 1500, '出售鱼', 0.8)
saveFishBtn = clickObj(700,1520, '放入水族馆', 0.5)

