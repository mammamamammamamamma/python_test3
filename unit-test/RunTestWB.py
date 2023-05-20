# -*- coding:utf-8 -*-
"""
作者：myx
日期：2023年05月11日 18:41
"""

from HTMLTestRunner import HTMLTestRunner
import unittest

testSuite = unittest.defaultTestLoader.discover('./',pattern='testWB.py')
with open('./report/testWB.html','wb') as f:
    HTMLTestRunner(stream=f,verbosity=2,title='微博登录及发布超话测试报告',description='20215120707马宇旋').run(testSuite)