import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from Common.handle_path import REPORT_DIR
from Common.handle_config import conf


"""
qq邮箱：530740300@qq.com
授权码：dtluwxbjpqrqbjba
qq邮箱的smtp服务器地址：smtp.qq.com,端口：465
"""


class Send_email:
    @staticmethod
    def sendEmail():
        # 1.连接smtp服务器,并登陆
        smtp = smtplib.SMTP_SSL(conf.get("EMAIL", "host"), conf.get("EMAIL", "port"))
        smtp.login(conf.get("EMAIL", "user"), conf.get("EMAIL", "password"))

        # 2.构造一封多组件邮件
        msg = MIMEMultipart()
        msg["Subject"] = conf.get("EMAIL", "subject")
        msg["To"] = conf.get("EMAIL", "To")
        msg["From"] = conf.get("EMAIL", "From")

        # 构造邮件的文本内容
        text = MIMEText("邮件中的文本内容", _charset="utf8")
        msg.attach(text)
        # 构造邮件的附件
        with open(os.path.join(REPORT_DIR, "report.html"), "rb") as f:
            content = f.read()
        report = MIMEApplication(content, _subtype='octet-stream')
        report.add_header('content-disposition', 'attachment', filename='自动化测试报告.html')
        msg.attach(report)

        # 3.发送邮件
        smtp.send_message(msg, from_addr=conf.get("EMAIL", "from_addr"), to_addrs=conf.get("EMAIL", "to_addrs"))






