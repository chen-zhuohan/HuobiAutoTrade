from conditions.model import Conditions


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
    if name == 'always_true' or name == '' or name is None:
        return always_true
    elif name == 'always_false':
        return always_false
    else:
        query_str = f'%{name}%'
        condition = Conditions.query.filter_by(Conditions.name.like(query_str)).first()
        if condition is None:
            return always_false
        else:
            return condition.is_valid


def get_or_create_condition(name) -> Conditions:
    query_str = f'%{name}%'
    condition = Conditions.query.filter(Conditions.name.like(query_str)).first()
    if not condition:
        condition = Conditions.create(name=name, valid=True)
    return condition
