# -*- coding:utf-8 -*-
"""
作者：myx
日期：2023年05月11日 18:31
"""

# 导包
import unittest
from HTMLTestRunner import HTMLTestRunner

import win32gui
import win32con
import time
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from logn import CookieLogin

# 登录微博
class TestLogn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        # 窗口最大化
        cls.driver.maximize_window()
        # 打开微博页面
        url = 'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F'
        cls.driver.get(url)
        sleep(1)
        # 设置元素等待
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # 关闭浏览器驱动
        sleep(2)
        cls.driver.quit()

    def test_logn(self):
        driver = self.driver
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 点击登录按钮
        driver.find_element(By.XPATH, '//*[@id="__sidebar"]/div/div[2]/div[1]/div/button').click()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(2)
        # 点击账号登录
        driver.find_element(By.XPATH, '//*[@id="app"]/div[5]/div[1]/div/div[2]/div/div/div[5]/a[1]').click()
        # 切换窗口
        # #获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        # 定位账号输入框
        uname = driver.find_element(By.XPATH, '//*[@id="loginname"]')
        uname.clear()
        uname.send_keys('13267872396')
        sleep(1)
        # 定位密码框
        password = driver.find_element(By.XPATH, '//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
        password.clear()
        password.send_keys('Ma13267872396')
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)
        # 点击登录按钮
        driver.find_element(By.XPATH, '//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)
# 发布微博
class TestWB(unittest.TestCase):
    # 定义初始化对象
    @classmethod
    def setUpClass(cls):
        # 免密登录微博账号
        prefs = {
            'profile.default_content_setting_values': {
                # 隐藏chromedriver的通知
                'notifications': 2
            },
            # 隐藏chromedriver自带的保存密码功能
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False
        }
        # 创建一个配置对象
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(service=Service(r'C:\python\python3.10\chromedriver.exe'), options=options)
        # 最大化窗口
        cls.driver.maximize_window()
        # 新浪微博网址
        url = "https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F"
        cls.driver.get(url)
        sleep(6)
        # 截屏（使用时间戳命名）
        cls.driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 设置元素等待
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # 关闭浏览器驱动
        sleep(2)
        cls.driver.quit()

    # 从新刷新进入新浪微博网址登陆成功
    def test_Along(self):
        driver = self.driver
        url = "https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F"
        driver.get(url)
        sleep(4)
        driver.delete_all_cookies()
        # 持久化登录，之后登录就不需要上面的扫二维码验证了
        login = CookieLogin("cookie.json")
        cookies = login.load_cookies()
        try:
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.weibo.com',
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": '',
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False
                }
                driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)
        sleep(3)
        driver.refresh()
        sleep(3)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')

    # 添加话题
    def test_Btalk(self):
        driver = self.driver
        # 切换窗口
        # 获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        # 定位话题按钮
        # 获得焦点
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[1]/div/div[4]/div').click()
        sleep(2)
        ele = driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[1]/div/textarea')
        ele.send_keys('完美世界七神下界最后一战')
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 按下回车键
        ele.send_keys(Keys.ENTER)
        sleep(1)

    # 文本域输入内容
    def test_Crelease(self):
        driver = self.driver
        # 切换窗口
        # 获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        # 定位分享输入框输入内容
        driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[1]/div/textarea').send_keys('完美世界更新啦，史上最长时长达到35分钟，七神下界最后一神，石昊底牌尽出仍不敌黄羽，鏖战许久，石昊活祭至尊骨，与神同归于尽，七神至此尽灭，真是国漫巅峰之作！')
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(2)

    # 点击表情添加表情（滚动条操作）
    def test_Dscroll(self):
        driver = self.driver
        driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[1]/div/div[1]/div').click()
        # 定位div
        scroll = driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[5]/div[1]/div/div/div[2]')
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)
        driver.execute_script("arguments[0].scrollIntoView(false)", scroll)
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 操作div
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[5]/div[1]/div/div/div[2]/div[2]/div/div[118]/div').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(2)

    # 上传图片
    def test_EputFile(self):
        driver = self.driver
        # 定位上传图片按钮
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[1]/div/div[2]/div/span/div').click()
        sleep(3)
        # 打开系统的Windows窗口，从窗口选择本地文件添加
        # 一级顶层窗口
        dialog = win32gui.FindWindow("#32770", "打开")
        # 二级窗口
        comboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)
        # 三级窗口
        comboBox = win32gui.FindWindowEx(comboBoxEx32, 0, "ComboBox", None)
        # 四级窗口 -- 文件路径输入区域
        edit = win32gui.FindWindowEx(comboBox, 0, "Edit", None)
        # 二级窗口 -- 打开按钮
        button = win32gui.FindWindowEx(dialog, 0, "Button", None)
        # 1、输入文件路径
        filepath = "D:\图片\wallpaper\完美世界石昊.jpg"
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 2、点击打开按钮
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    # 发布超话
    def test_Fsending(self):
        driver = self.driver
        # 点击发送按钮
        driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[4]/button').click()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    # 点击个人主页
    def test_Gmy(self):
        driver = self.driver
        driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a[5]/div/div/div/div').click()
        # 切换窗口
        # 获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

if __name__ == '__main__':
    testSuite = unittest.defaultTestLoader.discover('./', pattern='testWB.py')
    with open('./report/testWB.html', 'wb') as f:
        HTMLTestRunner(stream=f, verbosity=2, title='微博登录及发布超话测试报告', description='20215120707马宇旋').run(
            testSuite)