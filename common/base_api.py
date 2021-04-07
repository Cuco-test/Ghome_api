# coding:utf-8
import json,os
import requests
from Ghome_api.common.readexcel import ExcelUtil
from Ghome_api.common import resultdata
from Ghome_api.common.writeexcel import copy_excel, Write_excel
from common.Logs import Log
log = Log(__name__)
logger = log.Logger


def send_requests(s, testdata):
    '''封装requests请求'''
    true = True
    method = testdata["method"]
    url = testdata["url"]
    # url后面的params参数

    try:
        params = eval(testdata["params"])
    except:
        params = None

    try:
        files = eval(testdata["files"])
    except:
        files = None

    # 请求头部headers
    try:
        headers = eval(testdata["headers"])
        logger.info("请求头部：%s" % headers)
    except:
        headers = None
    # post请求body类型
    type = testdata["type"]

    test_nub = testdata['id']
    logger.info("*******正在执行用例：-----  %s  ----**********" % test_nub)
    logger.info("请求方式：%s, 请求url:%s" % (method, url))
    logger.info("请求params：%s" % params)
    # print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    # print("请求方式：%s, 请求url:%s" % (method, url))
    # print("请求params：%s" % params)

    # post请求body内容
    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata = {}

    # 判断传data数据还是json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata
    if method == "post": print("post请求body类型为：%s ,body内容为：%s" % (type, body))
    logger.info(("post请求body类型为：%s ,body内容为：%s" % (type, body)))

    verify = False
    res = {}   # 接受返回数据

    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      files=files,
                      headers=headers,
                      data=body,
                      verify=verify
                       )
        logger.info("页面返回信息：%s" % r.content.decode("utf-8"))
        res['id'] = testdata['id']
        res['rowNum'] = testdata['rowNum']
        res["statuscode"] = str(r.status_code)  # 状态码转成str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""


        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            logger.info("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        else:
            res["result"] = "fail"
            logger.info("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        return res


    except Exception as msg:
        res["msg"] = str(msg)
        return res

def wirte_result(result, filename="result.xlsx"):
    # 返回结果的行数row_nub
    row_nub = result['rowNum']
    # 写入statuscode
    wt = Write_excel(filename)
    wt.write(row_nub, 9, result['statuscode'])        # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 10, result['times'])             # 耗时
    wt.write(row_nub, 11, result['error'])            # 状态码非200时的返回信息
    wt.write(row_nub, 13, result['result'])           # 测试结果 pass 还是fail
    wt.write(row_nub, 14, result['msg'])              # 抛异常

if __name__ == "__main__":
    data = ExcelUtil("../case/GHome_api.xlsx").dict_data()
    # print(data[0])
    # print(type(data[0]))
    logger.info(data[0]["checkpoint"])
    logger.info(type(json.loads(data[0]["checkpoint"])))
    s = requests.session()
    res = send_requests(s, data[0])
    copy_excel("../case/GHome_api.xlsx", "result.xlsx")
    wirte_result(res, filename="result.xlsx")