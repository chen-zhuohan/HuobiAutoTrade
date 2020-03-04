from common.email_helper import send_error


class TaskTemplateBase:
    MSG_ARGS = tuple()
    MSG_FORMAT = ''

    RULE = ''

    def __str__(self):
        if len(self.MSG_ARGS) == 0:
            result = '未运行: {}'.format(self.RULE)
        else:
            try:
                result = self.MSG_FORMAT.format(self.MSG_ARGS)
                result = '运行结束: {}\n{}'.format(self.RULE, result)
            except Exception as e:
                result = '赋值msg失败: {}\n{}, {}'.format(self.RULE, self.MSG_ARGS, self.MSG_FORMAT)
                send_error(e)

        return result

    def try_pass(self, *args, **kwargs) -> bool:
        raise Exception('must be covered')