

def always_true(*args, **kwargs):
    return True


def always_false(*args, **kwargs):
    return False


def get_condition_by_name(name: str) -> callable:
    if name == 'always_true':
        return always_true
    elif name == 'always_false':
        return always_false