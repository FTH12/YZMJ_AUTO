import json
import re
import time
import cv2
import easyocr

from clickObj import *

reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # 设置语言（中文简体和英文）
def showMenu():
    print('********************')
    print('1: 熟练度（自己选英雄）')
    print('2: 钓鱼')
    print('3: 接管当前游戏')
    print('4: 看广告获取体力（每天一遍）')
    print('exit: 退出')
    print('********************')



def gotoUnit(driver, unit=1):
    if unit == 1:
        for i in range(43):
            unitLeft.click(driver)
    else:
        for i in range(unit-1):
            unitRight.click(driver)

def gotoHome(driver):
    homeBtn1.click(driver)
    homeBtn2.click(driver)
    print('回到主页')


# # 点击开始游戏，获取秘宝，选择技能等操作
# def preStartGame(driver):

def startGame(driver, hasQuan=False):
    startGameBtn.click(driver)
    startGameBtn1.click(driver)
    if hasQuan:
        target = clickObj(550, 950, '技能', 0.5)
    else:
        getAllBtn.click(driver)
        time.sleep(35)  # 看广告
        skipVideo(driver)

    for i in range(4):
        result = getShotResult(driver)
        selectJineng(driver, result)
        time.sleep(1)
    beisuBtn.click(driver)
    time.sleep(5)
    beisuBtn.click(driver)
    return monitor(driver)




def monitor(driver):
    monitorTime = 5
    while True:
        result = getShotResult(driver)
        jinengFlag = 0
        isInGame = False
        for detection in result:
            text = detection[1]
            if '获得秘卷' in text:
                mijuanBtn.click(driver)
                mijuanBtn.click(driver)
                jinengFlag = 0
                break
            elif '获得秘宝' in text:
                solveMb(driver, result)
                jinengFlag = 0
                break
            elif '选择技能' in text:
                selectJineng(driver, result)
                jinengFlag = 0
                break
            elif '领取奖励' in text:
                getPriceBtn.click(driver)
                print('********已通关********')
                time.sleep(2)
                result = getShotResult(driver)
                tl = 0
                for detection in result:
                    if '/60' in detection[1]:
                        tl = detection[1].split('/')[0]
                        break
                print('***** 剩余',tl, '点体力!')
                return tl
            else:
                jinengFlag += 1

        if jinengFlag>=3:
            jinengBtn1.click(driver)
            jinengBtn2.click(driver)
            clickObj(520,920,'屏幕中心1', 0.2, 100).click(driver)
            clickObj(550, 1380, '屏幕中心2', 0.2, 100).click(driver)
            jinengFlag = 0

        time.sleep(monitorTime)

def selectJineng(driver, result):
    # 想用的技能列表
    jinengList = ['激光', '御剑', '星链', '飞花']
    # 遍历结果
    for detection in result:
        for jineng in jinengList:
            if jineng in detection[1]:
                x, y = get_center(detection[0])
                target = clickObj(x, y, detection[1], 0.5)
                target.click(driver)
                return
    target = clickObj(550, 950,'技能' ,0.5)
    target.click(driver)

def getShotResult(driver):
    shotPath = 'screenshot.png'
    driver.save_screenshot(shotPath)
    image = cv2.imread(shotPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(shotPath, gray)
    result = reader.readtext(shotPath)
    return result

def skipVideo(driver):
    skipBtn.click(driver)
    # 判断广告是否退出
    flag = True
    while flag:
        tres = getShotResult(driver)
        for detection in tres:
            if '波数' in detection[1]:
                flag = False
                break
            elif 'X3' in detection[1]:
                flag = False
                break
            elif '无伤' in detection[1]:
                flag = False
                break
            elif '选择技能' in detection[1]:
                flag = False
                break
            elif '获得秘宝' in detection[1]:
                flag = False
                break
            elif '获得奖励' in detection[1]:
                flag = False
                break
        if flag:
            skipBtn.click(driver)
        time.sleep(2)



def solveMb(driver, result):

    hasVideo = False
    for detection in result:
        if '免费刷新' in detection[1]:
            x, y = get_center(detection[0])
            target = clickObj(x, y, '免费刷新',0.8)
            target.click(driver)
            hasVideo = True
            break
    if hasVideo:
        time.sleep(35)
        skipVideo(driver)


    confirmMb.click(driver)
    confirmMb.click(driver)

def continueGame(driver):
    return monitor(driver)


# 计算文字的中心点
def get_center(bbox):
    """
    根据边界框坐标计算中心点
    :param bbox: 边界框坐标，格式为 [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    :return: 中心点坐标 (center_x, center_y)
    """
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]
    center_x = sum(x_coords) // len(x_coords)
    center_y = sum(y_coords) // len(y_coords)
    return center_x, center_y


def isRunning(driver):
    pass


def gotoCity(driver):
    cityBtn.click(driver)
    print('进入城镇页')

def toFish(driver):
    gotoCity(driver)
    houseBtn.click(driver)
    diaoBtn.click(driver)
    print('进入钓鱼界面')

def startFish(driver, power=60):
    with open('fishInfo.json', 'r', encoding='utf-8') as f:
        fishInfo = json.load(f)
        print('*******当前鱼信息********')
        print(fishInfo)
        print('***********************')
    for i in range(power):
        startFishBtn.click(driver)
        time.sleep(1.5)
        result = getShotResult(driver)
        fishName = None
        for detection in result:
            # 如果鱼是目标鱼
            if detection[1] in ['鲸鲨', '灵魂鱼']:
                fishName = detection[1]
                continue
            if fishName:
                match = re.search(r"(?<=长度:  )\d+\.\d+(?=厘米)", detection[1])
                if match:
                    number = match.group()  # 获取匹配的数字
                    fishInfo[fishName].sort(key=lambda x:x['size'])
                    if float(number) > fishInfo[fishName][0]['size']:
                        print(f'*****{fishName}:{number}cm,大于 {fishInfo[fishName][0]['size']}!')
                        saveFishBtn.click(driver)
                        site = fishInfo[fishName][0]['site']
                        repalceBtn = clickObj(site[0],site[1],'替换鱼', 0.5)
                        repalceBtn.click(driver)
                        fishInfo[fishName][0]['size'] = float(number)
                    break

        sellBtn.click(driver)
        sellBtn.click(driver)
    with open('fishInfo.json', 'w', encoding='utf-8') as f:
        json.dump(fishInfo, f, ensure_ascii=False, indent=4)

def finishFish(driver):
    unitBack.click(driver)
    unitBack.click(driver)
    gotoHome(driver)
    print('-----钓鱼完成并返回-----')


def getTlByVideo(driver):
    result = getShotResult(driver)
    target = None
    for detection in result:
        if '/60' in detection[1]:
            x, y = get_center(detection[0])
            target = clickObj(x, y, '体力位置', 1, 150)
            break
    mfFlag = True
    while mfFlag:
        target.click(driver)
        tres = getShotResult(driver)
        mfFlag = False
        for det in tres:
            if '免费' in det[1]:
                mfFlag = True
                x, y = get_center(det[0])
                mfTarget = clickObj(x, y, '免费体力', 0.5, 200)
                mfTarget.click(driver)
                time.sleep(35)
                skipVideo(driver)
                clickObj(980, 1170, '确认领取体力', 0.3, 100).click(driver)

    print('****体力领取完成*****')
    clickObj(140, 1600, '体力领取完成点击', 0.3, 100).click(driver)