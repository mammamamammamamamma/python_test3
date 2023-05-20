# -*- coding:utf-8 -*-
"""
作者：myx
日期：2023年05月11日 20:59
"""
import time
from time import sleep
from lxml import etree
from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By

class TestBaidu():
    # 在类中的开始执行方法
    def setup_class(self):
        self.driver = webdriver.Chrome()
        # 窗口最大化
        self.driver.maximize_window()
        # 访问百度翻译页面
        self.driver.get('https://fanyi.baidu.com/')
        # 隐性等待
        self.driver.implicitly_wait(10)

    # 在类中的结束执行方法
    def teardown_class(self):
        sleep(2)
        # 关闭浏览器
        self.driver.quit()

    def test_01_popup(self):
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
            assert span != None
        else:
            print('无弹窗')
            assert span == None
        sleep(1)

    # 英文翻译为中文
    def test_02_fanyi(self):
        driver = self.driver
        # 定位翻译文本输入框
        txt = driver.find_element(By.XPATH, '//*[@id="baidu_translate_input"]')
        txt.click()
        # 输入要翻译的内容
        txt.send_keys('python')
        sleep(1)
        # 点击翻译
        driver.find_element(By.XPATH, '//*[@id="translate-button"]').click()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

     # 使用cookice登录百度账号
    def test_03_long(self):
        driver = self.driver
        # 添加cookice
        driver.add_cookie({'name': 'BDUSS',
                           'value': 'EY1N1pXNHpXN35PYjI1Mk1uSkNRTk42Z0dmUVNZQk9wNkhrWEZueU56bjMxV2xrSVFBQUFBJCQAAAAAAAAAAAEAAABWBnCHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPdIQmT3SEJkN'})
        # 刷新页面登录成功
        driver.refresh()
        sleep(2)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        sleep(1)

    # 添加笔记
    def test_04_notes(self):
        driver = self.driver
        # 定位笔记按钮
        # driver.find_element(By.XPATH,'//*[@id="main-outer"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/a[4]').click()
        sleep(1)
        # 输入笔记
        ele = driver.find_element(By.XPATH,'//*[@id="noteContainer"]/div/div[1]/div[1]/textarea')
        ele.clear()
        ele.send_keys('这是做实验的时候做的笔记')
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 点击保存按钮
        driver.find_element(By.XPATH,'//*[@id="noteContainer"]/div/div[2]/a').click()
        sleep(1)
        # 截屏（使用时间戳命名）
        driver.get_screenshot_as_file(f'./img/百度翻译{time.strftime("%Y_%m_%d %H_%M_%S")}.png')
        # 获取当前页面源码
        page = driver.page_source
        tree = etree.HTML(page)
        a = tree.xpath('//*[@id="noteContainer"]/div/div[2]/a[@class="saveBtn saveBtnDisable"]')
        # 断言
        if a != None:
            print('保存成功')
            assert a != None
        else:
            print('保存失败')
            assert a == None
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="main-outer"]/div/div/div[1]/div[1]/div[4]/a[1]').click()
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
    pytest.main(['-s', '-q', '--alluredir', './report/'])