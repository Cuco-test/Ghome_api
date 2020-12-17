# coding:utf-8
import unittest
import ddt
import os
import requests
from Ghome_api.common import base_api
from Ghome_api.common import readexcel
from Ghome_api.common import writeexcel
from Ghome_api.common.logger import Log
log = Log()

log.info("")
log.info("获取GHome_api.xlsx路径")
curpath = os.path.dirname(os.path.realpath('__file__'))
testxlsx = os.path.join(curpath, "GHome_api.xlsx")


log.info("report_路径确认")
report_path = os.path.join(curpath, "report")
reportxlsx = os.path.join(report_path, "result.xlsx")

writeexcel.copy_excel(testxlsx, reportxlsx)

testdata = readexcel.ExcelUtil(testxlsx).dict_data()
@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        # 如果有登录的话，就在这里先登录了
        writeexcel.copy_excel(testxlsx, reportxlsx)
        log.info("复制GHome_api.xlsx文件到report下")

    @ddt.data(*testdata)
    def test_001(self, data):
        # 先复制excel数据到report
        res = base_api.send_requests(self.s, data)

        base_api.wirte_result(res, filename=reportxlsx)
        # 检查点 checkpoint
        check = data["checkpoint"]
        log.info("检查点确认")
        print("检查点->：%s"%check)
        # 返回结果
        res_text = res["text"]
        log.info("实际返回值确认")
        print("返回实际结果->：%s"%res_text)
        # 断言
        log.info("判断返回值是否正常")
        self.assertTrue(check in res_text)




if __name__ == "__main__":


    unittest.main()

