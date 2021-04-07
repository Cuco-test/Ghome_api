
# -*-coding:utf-8-*-

import pymysql,os,sys
from common.Logs import Log
from config import readConfig
file = os.path.basename(sys.argv[0])
log = Log(file)
logger = log.Logger

try:
    conn = pymysql.connect(
        host="fe-db.cjcmlkqmw47g.us-west-2.rds.amazonaws.com",
        port=3306,
        user="FEKeeper",
        password="kNyU4LHVBJepIr4qOzNY",
        #database="iot-server",
        database="iot-server-common-app",
        charset='utf8'
        )
    cur = conn.cursor()
    logger.info("-----------------------连接数据库成功----------------------------------")
except:
    logger.warn("-----------------------连接数据库失败-------------------------------")


def add_data(sql,param):
    # 添加数据数据
    person = [['username', '86-18680667585',''], ['username', '86-18680667588']]
    for i in range(len(person)):
        param = tuple(person[i])
        # 执行sql语句
        count = cur.execute(sql, param)
        # 判断是否成功
        if count > 0:
            logger.info("-----------------------添加数据成功-------------------------------")


def delete_data(sql):
    conn.ping(reconnect=True)
    cur.execute(sql)
    logger.info("-----------------------数据库命令执行成功-------------------------------")
    users = cur.fetchall()
    conn.commit()
    for i in range(len(users)):
        logger.info(users[i])



def control_data(sqllist):
    #sqllist = []
    try:
        for sql in sqllist:
            delete_data(sql)
        logger.info("-----------------------数据库操作完成---------------------------")
    except:
        logger.warn("-----------------------数据库操作异常---------------------------")
    cur.close()
    conn.close()
    logger.info("-----------------------断开数据库成功----------------------------------")

if __name__ == "__main__":
    path = os.path.dirname(os.getcwd()) + '\\config\\cfg.ini'
    sqllist = readConfig.dataconfig(path,"sqlcontrol")
    print(sqllist)
    control_data(sqllist)



