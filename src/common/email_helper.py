import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from configs import USERS, MAIL_HOST, MAIL_PASSWORD, MAIL_PORT, MAIL_USER, TESTING
import logging

DEFAULT = list(USERS.values())    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
MANAGERS = USERS['czh']
log = logging.getLogger(__name__)


def _make_smtp():
    smtpObj = smtplib.SMTP()
    smtpObj.connect(MAIL_HOST, MAIL_PORT)
    smtpObj.login(MAIL_USER, MAIL_PASSWORD)
    log.info('make smtp successfully')
    return smtpObj


def _send_all(smtpObj, msg, receivers):
    if isinstance(receivers, str):
        receivers = (receivers, )

    if isinstance(receivers, (list, tuple)):
        for receiver in receivers:
            msg['To'] = receiver
            if not TESTING:
                smtpObj.sendmail(MAIL_USER, receiver, msg.as_string())
                log.info('send email to {} successfully'.format(receiver))
    else:
        msg = 'Receivers must be str, list or tuple, but receive {}'.format(type(receivers))
        log.error(msg)
        raise TypeError(msg)


def send_email(title, context, receivers=DEFAULT):
    title = '【来自陈卓涵的火币监控】 {}'.format(title)
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = MAIL_USER
    msg.attach(MIMEText(context, 'plain', 'utf-8'))
    try:
        smtpObj = _make_smtp()
        _send_all(smtpObj, msg, receivers)
    except smtplib.SMTPException as e:
        log.error('send email fail, detail: {}, {}'.format(e, e.args))


def send_error(error: Exception, extra: str = None):
    title = '程序运行错误！'
    context = '{}\n{}\n{}'.format(extra, type(error), error.args)
    send_email(title, context, MANAGERS)


def send_task_pass(result):
    title = '阶段性通过！'
    send_email(title, str(result))


def send_missionary_pass(name: str):
    title = '任务链完成！'
    msg = '{} 的判断条件全部达成，并完成了最终目标，请及时检查！'.format(name)
    send_email(title, msg)


def send_trade(title, trade):
    context = str(trade)
    send_email(title, context)


if __name__ == '__main__':
    send_email('测试', 'detail')