import requests,hashlib,os,json




def get_login_token(username):
    #获取登录token
    headers = {'Content-Type':'application/x-www-form-urlencoded','platform':'huawei','lang':'en'}
    body = {'username':username,'password':'CUCO123456','region_code':'cn','phone_code':'86'}
    response = requests.post("https://test-feiot.gosund.com/v1.1/obtain_jwt_auth/", data=body, headers=headers)
    token = response.json()['data']['token']
    # print("登录token"+token)
    return token

def get_pair_tokenparams(username):
    #获取配网token信息
    headers = {'Authorization': 'JWT '+get_login_token(username)}
    body = {'timezoneId': "Asia/Shanghai", 'pairType': 'EZ'}
    response = requests.post("https://test-feiot.gosund.com/v1.1/devices/token/", data=body, headers=headers)
    params = response.json()['data']["pair"]
    print(params)
    return params

def get_pair_token(username):
    #配网token加密为pair_token
    params = get_pair_tokenparams(username)
    token =params["token"]
    secret = params["secret"]
    m5 = hashlib.md5()
    m5.update(token.encode(encoding='utf-8'))
    m5.update(secret.encode(encoding='utf-8'))
    return m5.hexdigest()

def test1(username):

    params = {'devices':'2f81870ea0df4bc8b1c4a5749d67130e'}

    headers = {'Authorization':"JWT "+get_login_token('JiangHuaQiang@gosund.com'),'lang':'en'}


    response = requests.get("https://test-feiot.gosund.com/v1.1/devices/ota_list/", params = params, headers=headers)
    print(response)

if __name__ == "__main__":
    test1('JiangHuaQiang@gosund.com')