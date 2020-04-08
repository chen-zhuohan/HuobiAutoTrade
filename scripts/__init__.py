import argparse

parser = argparse.ArgumentParser(description='script manage')
parser.add_argument('hi', type=str, help='action')
parser.add_argument('-n', '--name', type=str, help='your name')
parser.add_argument('-s', '--sex', type=str, choices=('man', 'woman'), help='your name')

args = parser.parse_args()
print('args: {}'.format(args))
print('hi: {}'.format(args.hi))
print('--name: {}'.format(args.name))
print('--sex: {}'.format(args.sex))
