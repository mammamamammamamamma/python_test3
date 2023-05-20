# -*- coding:utf-8 -*-
"""
作者：myx
日期：2023年05月11日 9:48
"""


# 导包
import unittest
import time
from HTMLTestRunner import HTMLTestRunner

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from lxml import etree


# 测试类
class TestBaidu(unittest.TestCase):
    # 定义初始化对象
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        # 窗口最大化
        cls.driver.maximize_window()
        # 打开百度翻译
        url = 'https://fanyi.baidu.com/'
        cls.driver.get(url)
        sleep(1)
        # 设置元素等待
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # 关闭浏览器驱动
        sleep(2)
        cls.driver.quit()
        print('全部测试已完成...')

    def test_01_Popup(self):
        driver = self.driver
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)
        # 获取当前页面源码
        page = driver.page_source
        # 解析当前源码
        tree = etree.HTML(page)
        span = tree.xpath('//*[@id="app-guide"]/div/div/div[2]/span')
        # 断言
        if span != None:
            print('有弹窗')
            # 关闭弹窗
            driver.find_element(By.XPATH, '//*[@id="app-guide"]/div/div/div[2]/span').click()
        else:
            print('无弹窗')
        sleep(1)

    # 英文翻译为中文
    def test_02_yingwen_fanyi(self):
        driver = self.driver
        # 定位翻译文本输入框
        txt = driver.find_element(By.XPATH, '//*[@id="baidu_translate_input"]')
        txt.click()
        # 输入要翻译的内容
        txt.send_keys('spider')
        sleep(1)
        # 点击翻译
        driver.find_element(By.XPATH, '//*[@id="translate-button"]').click()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    # 切换翻译语言，中文翻译为英文
    def test_03_zhongwen_fanyi(self):
        driver = self.driver
        # 点击切换语言
        driver.find_element(By.XPATH,'//*[@id="main-outer"]/div/div/div[1]/div[1]/div[1]/a[2]/span').click()
        # 定位输入框
        txt1 = driver.find_element(By.XPATH, '//*[@id="baidu_translate_input"]')
        txt1.clear()
        txt1.send_keys('自动化测试')
        # 点击翻译
        driver.find_element(By.XPATH, '//*[@id="translate-button"]').click()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    # 使用cookice登录百度账号
    def test_04_Dlong(self):
        driver = self.driver
        # 添加cookice
        driver.add_cookie({'name':'BDUSS','value':'EY1N1pXNHpXN35PYjI1Mk1uSkNRTk42Z0dmUVNZQk9wNkhrWEZueU56bjMxV2xrSVFBQUFBJCQAAAAAAAAAAAEAAABWBnCHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPdIQmT3SEJkN'})
        # 刷新页面登录成功
        driver.refresh()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    def test_05_Collect(self):
        driver = self.driver
        # 点击收藏按钮
        driver.find_element(By.XPATH,'//*[@id="main-outer"]/div/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div[1]/a/span').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 获取单前页面源码
        page = driver.page_source
        # 解析页面源码
        tree = etree.HTML(page)
        # 获取想要的内容
        ele = tree.xpath('//*[@id="main-outer"]/div/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div[1]/a/@title')[0]
        # 断言
        if ele == '取消收藏':
            print('收藏成功')
        else:
            print('收藏失败')
        driver.find_element(By.XPATH,'//*[@id="main-outer"]/div/div/div[1]/div[1]/div[4]/a[1]').click()
        sleep(1)
        # 切换窗口
        # 获取当前浏览器的所有窗口句柄
        handles = driver.window_handles
        # 切换到最新打开的窗口
        driver.switch_to.window(handles[-1])
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

if __name__ == '__main__':
    testSuite = unittest.defaultTestLoader.discover('./', pattern='testBaidu.py')
    with open('./report/testBaidu.html', 'wb') as f:
        HTMLTestRunner(stream=f, verbosity=2, title='百度翻译测试报告', description='20215120707马宇旋').run(testSuite)

