from argparse import ArgumentParser

from deadept import DeAdept
from deadept.platform import PlatformSelector

def run():
	selector = PlatformSelector()
	parser = ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('infile', type=str, help='Input epub file', nargs='?')
	group.add_argument('-l', action='store_const', const=True, dest='list', help='List available platforms')
	parser.add_argument('outfile', type=str, default=None, nargs='?', help='(optional) output file')
	parser.add_argument('-f', action='store_const', const=True, dest='force', help='Force writing of output to input file, this is here just to prevent accidental overwrites')
	parser.add_argument('-p', metavar='PLATFORM', type=str, dest='platform', choices=selector.platforms(), default=selector.default(), help=f'Platform to use for extracting the user key, the default is {selector.default()}')

	args = parser.parse_args()

	if args.list:
		print("Available platforms:")
		for platform in selector.platforms():
			print(platform)
		exit()

	if not args.outfile and not args.force:
		print("Output filename not specified, use -f to just replace input file.")
		exit()

	da = DeAdept(args.infile, args.platform)
	da.decrypt(args.outfile)
