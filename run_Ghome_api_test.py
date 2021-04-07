# coding=utf-8
import unittest
import time
from Ghome_api.common import HTMLTestRunner
import os
import sys
from common.Logs import Log
from Ghome_api.common import emails
#log = Log(__name__)
#logger = log.Logger

file = os.path.basename(sys.argv[0])
log = Log(file)
logger = log.Logger

curpath = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(curpath, "report")
if not os.path.exists(report_path): os.mkdir(report_path)
case_path = os.path.join(curpath, "case")
def add_case(casepath=case_path, rule="test*.py"):
    '''加载所有的测试用例'''
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath,
                                                  pattern=rule,)

    return discover

def run_case(all_case, reportpath=report_path):
    '''执行所有的用例, 并把结果写入测试报告'''
    htmlreport = reportpath+r"\result.html"
    logger.info("测试报告生成地址：%s"% htmlreport)
    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           verbosity=2,
                                           title="Cuco_GHome_api自动化测试报告",
                                           description="用例执行情况")

    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()

def sendemail(reportpath):
    new_report = emails.new_report(reportpath)
    emails.send_mail(new_report)  # 发送测试报告

if __name__ == "__main__":
    reportpath = "D:\\project\\Ghome_api\\report\\"
    logger.info("开始执行脚本")
    cases = add_case()
    run_case(cases)
    # sendemail(reportpath)