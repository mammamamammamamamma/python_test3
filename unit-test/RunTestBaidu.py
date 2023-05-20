# -*- coding:utf-8 -*-
"""
作者：myx
日期：2023年05月11日 18:22
"""
from HTMLTestRunner import HTMLTestRunner
import unittest

testSuite = unittest.defaultTestLoader.discover('./',pattern='testBaidu.py')
with open('./report/testBaidu.html','wb') as f:
    HTMLTestRunner(stream=f,verbosity=2,title='百度翻译测试报告',description='20215120707马宇旋').run(testSuite)