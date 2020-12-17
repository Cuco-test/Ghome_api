# 预期结果
expected = {'username':'kaishui'}
# 实际结果
result={
    'code': 1 ,
    'username':'kaishui',
    'token':'ihbedvbwejhvkjvberkjvbkjgkesjvbbje'
}

for key in testdata["checkpoint"]:
    if (key in ["text"]) & (["text"] == ["checkpoint"]):
        res["result"] = "pass"
        print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))

    else:
        res["result"] = "fail"
        print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))