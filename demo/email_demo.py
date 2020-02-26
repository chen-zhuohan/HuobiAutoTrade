import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1185671574@qq.com"  # 用户名
mail_pass = "fjrhahmxiavgidei"  # 口令
port = 587

sender = '1185671574@qq.com'
DEFAULT = ('1582544942@qq.com', '1185671574@qq.com')  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
CZH = ('1185671574@qq.com', )


def send_email(title, context, receivers=CZH):
    title = '【来自陈卓涵的火币监控】 {}'.format(title)
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = sender
    msg.attach(MIMEText(context, 'plain', 'utf-8'))
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, port)
        smtpObj.login(mail_user, mail_pass)
        for receiver in receivers:
            msg['To'] = receiver
            smtpObj.sendmail(sender, receiver, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(str(e.args))
        print("Error: 无法发送邮件")