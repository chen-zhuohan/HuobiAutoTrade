

def always_true(*args, **kwargs):
    return True


def always_false(*args, **kwargs):
    return False


def get_condition_by_name(name: str) -> callable:
    """
    空字符串 always True

    :param name:
    :return:
    """
    if name == 'always_true':
        return always_true
    elif name == 'always_false':
        return always_false
    elif name == '':
        return always_true