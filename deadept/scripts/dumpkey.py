from argparse import ArgumentParser

from deadept import DeAdept
from deadept.platform import PlatformSelector

def run():
	selector = PlatformSelector()
	parser = ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-l', action='store_const', const=True, dest='list', help='List available platforms')
	group.add_argument('-p', metavar='PLATFORM', type=str, dest='platform', choices=selector.platforms(), default=selector.default(), help=f'Platform to use for extracting the user key, the default is {selector.default()}')

	args = parser.parse_args()

	if args.list:
		print("Available platforms:")
		for platform in selector.platforms():
			print(platform)
		exit()

	da = DeAdept(None, args.platform)
	key = da.getKey()

	with open('adept.der', 'bw') as fp:
		fp.write(key.export_key('DER'))
