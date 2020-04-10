import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

"""
qq邮箱：530740300@qq.com
授权码：dtluwxbjpqrqbjba
qq邮箱的smtp服务器地址：smtp.qq.com,端口：465

"""
#1.连接smtp服务器,并登陆
smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)
smtp.login(user="530740300@qq.com", password="dtluwxbjpqrqbjba")

#2.构造一封多组件邮件
msg = MIMEMultipart()
msg["Subject"] = "测试邮件01"
msg["To"] = "lemonban@qq.com"
msg["From"] = "530740300@qq.com"

#构造邮件的文本内容
text = MIMEText("邮件中的文本内容", _charset="utf8")
msg.attach(text)
# 构造邮件的附件
with open(r"C:\Users\Administrator\Desktop\Api_test\Reports\report.html", "rb") as f:
    content = f.read()
report = MIMEApplication(content, _subtype='octet-stream')
report.add_header('content-disposition', 'attachment', filename='python.html')
msg.attach(report)

#3.发送邮件
smtp.send_message(msg, from_addr="530740300@qq.com", to_addrs=["530740300@qq.com", "18562576336@163.com"])


