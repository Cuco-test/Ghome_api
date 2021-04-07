# coding:utf-8
import unittest
import ddt
import os
import requests
from Ghome_api.common import base_api
from Ghome_api.common import readexcel
from Ghome_api.common import writeexcel
from Ghome_api.common import mysql
from Ghome_api.config import readConfig
from common.Logs import Log
log = Log(__name__)
logger = log.Logger
path = os.path.dirname(os.getcwd()) + "\\Ghome_api\\config\\cfg.ini"
reportpath  = os.path.dirname(os.getcwd()) +'\\Ghome_api\\report\\'





# 获取Ghome_api.xlsx路径
curpath = os.path.dirname(os.path.realpath(__file__))
testxlsx = os.path.join(curpath, "Ghome_api.xlsx")


# 复制Ghome_api.xlsx文件到report下
report_path = os.path.join(os.path.dirname(curpath), "report")
reportxlsx = os.path.join(report_path, "result.xlsx")

testdata = readexcel.ExcelUtil(testxlsx).dict_data()
@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        # 如果有登录的话，就在这里先登录了
        writeexcel.copy_excel(testxlsx, reportxlsx) # 复制xlsx
        #删除账号
        select = "sqlcontrol"
        #mysql.control_data(readConfig.dataconfig(path,select))


    @ddt.data(*testdata)
    def test_GHome_api(self, data):
        # 先复制excel数据到report
        res = base_api.send_requests(self.s, data)

        base_api.wirte_result(res, filename=reportxlsx)
        # 检查点 checkpoint
        check = data["checkpoint"]
        logger.info("检查点->：%s"%check)
        # 返回结果
        res_text = res["text"]
        logger.info("返回实际结果->：%s"%res_text)
        print("检查点->：%s"%check)
        print("返回实际结果->：%s"%res_text)
        # 断言
        self.assertTrue(check in res_text)

if __name__ == "__main__":
    unittest.main()