import inspect
from common.email_helper import send_error
from common.utils import Logger

logger = Logger('task template')


class TaskTemplateBase:
    RULE = ''
    MSG_FORMAT = ''

    def __init__(self, *args, **kwargs):
        self.msg_args = tuple()
        self.need_record = True

    def __str__(self):
        return self.msg

    def try_pass(self, *args, **kwargs) -> bool:
        raise Exception('must be covered')

    @classmethod
    def get_args(cls):
        return str(inspect.getfullargspec(cls.try_pass).args[1:])
        # return str(cls.try_pass.__code__.co_varnames[1:])   # exclude self

    @property
    def msg(self):
        if len(self.msg_args) == 0:
            result = '[Task Temp未运行: {}]'.format(self.RULE)
        else:
            try:
                msg = self.MSG_FORMAT.format(*self.msg_args)
                result = '[Task Temp运行结束: {}]'.format(msg)
            except Exception as e:
                result = '[Task Temp赋值msg失败: {}, {}]'.format(self.msg_args, self.MSG_FORMAT)
                send_error(e)
        logger.info('get msg: {}'.format(result))
        return result

    @property
    def format_msg(self):
        if len(self.msg_args) == 0:
            result = '<Task Temp未运行>\n规则：{}'.format(self.RULE)
        else:
            try:
                result = self.MSG_FORMAT.format(self.msg_args)
                result = '<Task Temp运行结束>\n 规则：{}\n运行结果：{}'.format(self.RULE, result)
            except Exception as e:
                result = '<Task Temp赋值msg失败>\n规则：{}\n结果参数{}\n结果模板{}'.format(self.RULE, self.msg_args, self.MSG_FORMAT)
                send_error(e)

        return result
