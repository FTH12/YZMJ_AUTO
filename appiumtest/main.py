import base64
import os
import time
from appium import webdriver
from appium.webdriver.webdriver import ExtensionBase
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from orders import *



# 初始化 PaddleOCR
# ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 设置语言为中文


# screenshot_path = 'screenshot.png'
# driver.save_screenshot(screenshot_path)


def initDriver():
  desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '7',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
    'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
    'appPackage': 'com.hardtime.yzmj.yongzhe',  # 启动APP Package名称
    'appActivity': 'com.hd.gamesdk.common.utils_ui.activity.SplashActivity',  # 启动Activity名称
    'unicodeKeyboard': True,  # 自动化需要输入中文时填True
    'resetKeyboard': True,  # 执行完程序恢复原来输入法
    'noReset': True,  # 不要重置App
    'newCommandTimeout': 6000,
    'automationName': 'UiAutomator2',
    # 'app': r'd:\apk\bili.apk',
  }
  # 连接Appium Server，初始化自动化环境
  driver = webdriver.Remote('http://localhost:4723',
                            options=UiAutomator2Options().load_capabilities(desired_caps))
  # 设置缺省等待时间
  driver.implicitly_wait(8)
  print('-----驱动初始化完成------')
  return driver


if __name__ == '__main__':
  driver = initDriver()
  flag = 1
  isSelectUnit = False # 是否已经选择了关卡
  hasQuan = False
  while (flag == 1):

    showMenu()
    isAllin = False
    order = input('输入指令：')
    if order == '1':
      temp = input('是否手动选择关卡： 1:是,2:否(手动选择完成后输入)\n')
      if temp == '1':
        isSelectUnit = True
      elif temp == '2':
        isSelectUnit = False
      temp = input('是否刷完体力? 1:是,2:否\n')
      if temp == '1':
        isAllin = True
      elif temp == '2':
        isAllin = False
      if isSelectUnit == False:
        gotoUnit(driver)
        gotoUnit(driver, 20)
        isSelectUnit = True
      temp = input('是否有广告券？ 1:是,2:否\n')
      if temp == '1':
        hasQuan = True
      tl = startGame(driver, hasQuan)
      if isAllin:
        while int(tl) >= 10:
          tl = startGame(driver, hasQuan)

    elif order == '2':
      toFish(driver)
      startFish(driver)
      finishFish(driver)
    elif order == '3':
      continueGame(driver)
    elif order == '4':
      getTlByVideo(driver)
    elif order == 'exit':
      driver.quit()
      break



