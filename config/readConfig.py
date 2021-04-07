
import configparser,sys,os
config = configparser.ConfigParser() # 类实例化
from common.Logs import Log
'''
file = os.path.basename(sys.argv[0])
log = Log(file)
logger = log.Logger
'''
path = os.path.dirname(os.getcwd()) +'\\config\\cfg.ini'


"""
# 第一种读取ini文件方式,通过read方法
config.read(path)
value = config['select']['url']
print('第一种方法读取到的值：',value)

# 第二种读取ini文件方式，通过get方法
value = config.get('select','url')
print('第二种方法读取到的值：',value)

# 第三种读取ini文件方式，读取到一个section中的所有数据，返回一个列表
value = config.items('select')
print('第三种方法读取到的值：',value)

# 将数据写入到ini文件中
config.add_section('login') # 首先添加一个新的section
config.set('login','username','admin')  # 写入数据
config.set('login','password','123456') # 写入数据
config.write(open(path,'a'))            #保存数据
"""


def readconfig(select,key):
    #读取单个配置文件
    config.read(path)
    value = config.get(select,key)
    print(value)
    return value

def readitem(path,select):
    #读取单个配置文件
    config.read(path)
    value = config.items(select)
    return value

def writeconfig(path,select,key,value):
    #添加配置文件
    config.read(path)
    section = config.sections()
    if select in section:
        print(select+"------已存在------，")
    else:
        config.add_section(select)
    config.set(select,key,value)
    config.write(open(path,"a"))

def dataconfig(path,select):
    #获取该分组所有的key
    sqllist = []
    list = readitem(path, select)
    for i in range(len(list)):
        data=list[i][1]
        #print(data)
        sqllist.append(data)
    # print(sqllist)
    return sqllist
def configselect(path,select):
    #获取该分组所有的key和value
    config.read(path)
    value =  dict(config.items(select))
    # print(value)
    return value

if __name__ == "__main__":
    #writeconfig('test', "username","123")
    # readconfig
    dataconfig(path,"sqlcontrol")

