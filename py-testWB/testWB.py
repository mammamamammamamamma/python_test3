# -*- coding:utf-8 -*-
"""
作者：myx
日期：2023年05月12日 12:59
"""


# 导包
import pytest
import time
from selenium import webdriver
from time import sleep
from lxml import etree
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from logn import CookieLogin

# 登录账号类
class TestLogn():
    def setup_class(self):
        self.driver = webdriver.Chrome()
        # 窗口最大化
        self.driver.maximize_window()
        # 打开微博页面
        url = 'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F'
        self.driver.get(url)
        sleep(1)
        # 设置元素等待
        self.driver.implicitly_wait(10)

    def teardown_class(self):
        # 关闭浏览器驱动
        sleep(2)
        self.driver.quit()

    def test_logn(self):
        driver = self.driver
        # 点击登录按钮
        driver.find_element(By.XPATH, '//*[@id="__sidebar"]/div/div[2]/div[1]/div/button').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)
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
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

# 发布微博类
class TestWB():
    # 定义初始化对象
    def setup_class(self):
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
        self.driver = webdriver.Chrome(service=Service(r'C:\python\python3.10\chromedriver.exe'), options=options)
        # 最大化窗口
        self.driver.maximize_window()
        # 新浪微博网址
        url = "https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F"
        self.driver.get(url)
        sleep(6)
        # 截屏（使用时间戳命名）
        self.driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 设置元素等待
        self.driver.implicitly_wait(10)

    def teardown_class(self):
        # 关闭浏览器驱动
        sleep(2)
        self.driver.quit()

    # 从新刷新进入新浪微博网址登陆成功
    def test_01_long(self):
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
        sleep(1)
        driver.refresh()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')

    # 添加话题
    def test_02_talk(self):
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
    def test_03_input(self):
        driver = self.driver
        # 切换窗口
        # 获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        # 定位分享输入框输入内容
        driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[1]/div/textarea').send_keys('完美世界更新啦，史上最长时长达到35分钟，七神下界最后一神，石昊底牌尽出仍不敌黄羽，鏖战许久，石昊活祭至尊骨，与神同归于尽，七神至此尽灭，真是国漫巅峰之作！')
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    # 设置发布时间
    def test_04_time(self):
        driver = self.driver
        # 点击定时微博
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[2]/div/i').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 鼠标悬停在时间上
        ele = driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[1]/span/input')
        ActionChains(driver).move_to_element(ele).perform()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 定位到5月13号
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[1]/span/div/div/div/div[1]/div[1]/div/div/div[2]/div[20]/div/div/span').click()
        sleep(1)
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 点击时间
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[3]').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[3]/div/div[1]').click()
        sleep(1)
        # 点击选择56分
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[3]/div/div[3]/ul/li[57]/span/span').click()
        sleep(1)
        # 点击发布按钮
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[4]/div/div[4]/button').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')

    # 编辑待发送的微博
    def test_05_edit(self):
        driver = self.driver
        sleep(1)
        # 刷新页面
        driver.refresh()
        # 执行js语句滑动滚动条
        driver.execute_script('window.scrollTo(0,1000)')
        sleep(3)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 点击编辑待发送的微博
        driver.find_element(By.XPATH,'//*[@id="__sidebar"]/div/div[2]/div/div[3]/a[3]/div/div[2]/div/div[1]/div/div[1]/div').click()
        sleep(1)
        # 切换窗口
        # 获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 点击立即发送按钮
        driver.find_element(By.XPATH,'//*[@id="scroller"]/div[1]/div/div/div/div[1]/div[2]/button[2]').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 点击确认
        driver.find_element(By.XPATH,'//*[@id="app"]/div[4]/div[1]/div/div[3]/button[2]').click()
        sleep(1)
        # 获取当前页面源码
        page = driver.page_source
        tree = etree.HTML(page)
        put = tree.xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/div/span')
        if put != None:
            print('发布成功')
            assert put != None
        else:
            print('发布失败')
            assert put == None
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/新浪微博{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)
        driver.get('https://weibo.com/u/7834002553')
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
    pytest.main(['-s', '-q', 'testWB.py', '--alluredir', './report/'])