# coding=utf-8


import os,time
from Ghome_api.config import readConfig
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
from common.Logs import Log
log = Log(__name__)
logger = log.Logger
path = os.path.dirname(os.getcwd()) + "\\Ghome_api\\config\\cfg.ini"


# ==============定义发送邮件==========
def send_mail(file_new):

    #-----------1.跟发件相关的参数------
    smtpserver = 'mail.gosund.com'                                   #发件服务器
    port = 465                                                       #端口
    username = 'JiangHuaQiang@gosund.com'                            #发件箱用户名
    password = '46H9KuQP'                                            #发件箱密码
    sender = 'JiangHuaQiang@gosund.com'                              #发件人邮箱
    receiver = readConfig.dataconfig(path, "emails")                 #收件人邮箱
    # ----------2.编辑邮件的内容------
    #读文件
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    # 邮件正文是MIMEText
    body = MIMEText(mail_body, 'html', 'utf-8')
    # 邮件对象
    msg = MIMEMultipart()
    msg['Subject'] = Header("Cuco_Ghome_api自动化测试报告", 'utf-8').encode()    #主题
    msg['From'] = Header(u'测试机器人 <%s>'%sender)                                 #发件人
    #msg['To'] = Header(u'测试负责人 <%s>'%receiver)                              #收件人
    msg['To'] = ';'.join(receiver)
    msg['date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")
    msg.attach(body)
    # 附件
    att = MIMEText(mail_body, "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename="result.html"'
    msg.attach(att)
    # ----------3.发送邮件------
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)  # 连服务器
        smtp.login(sender, password)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
        smtp.login(sender, password)  # 登录
    smtp.sendmail(sender, receiver, msg.as_string())  # 发送
    smtp.quit()
    # #发送邮件
    # smtp = smtplib.SMTP()
    # smtp.connect('smtp.mxhichina.com')  # 邮箱服务器
    # smtp.login(username, password)  # 登录邮箱
    # smtp.sendmail(sender, receiver, msg.as_string())  # 发送者和接收者
    # smtp.quit()
    logger.info("邮件已发出！注意查收。")
# ======查找测试目录，找到最新生成的测试报告文件======
def new_report(test_report):
    lists = os.listdir(test_report)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "\\" + fn))  # 按时间排序
    file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    logger.info(file_new)
    return file_new
if __name__ == "__main__":

    test_path = "D:\\project\\Ghome_api\\report\\"
    new_report = new_report(test_path)
    send_mail(new_report)  # 发送测试报告