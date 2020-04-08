from argparse import ArgumentParser, _SubParsersAction

parser = ArgumentParser(description='火币自动交易系统快捷管理系统')
subparsers = parser.add_subparsers(help='可选行为')


def register(subparsers: _SubParsersAction):
    parse = subparsers.add_parser('account')
    parse.add_argument('')