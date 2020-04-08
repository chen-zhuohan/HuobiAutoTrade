import argparse

parser = argparse.ArgumentParser(description='script manage')
subparsers = parser.add_subparsers(help='可选行为')
fuck_parse = subparsers.add_parser('fuck')

fuck_parse.add_argument('-n', '--name', type=str, help='your name')
fuck_parse.add_argument('-s', '--sex', type=str, choices=('man', 'woman'), help='your sex')
fuck_parse.register()


hi_parse = subparsers.add_parser('hi')

hi_parse.add_argument('-n', '--name', type=str, help='your name')

args = parser.parse_args()
print('args: {}'.format(args))
print('hi: {}'.format(args.hi))
print('--name: {}'.format(args.name))
print('--sex: {}'.format(args.sex))
