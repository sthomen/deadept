from argparse import ArgumentParser, _HelpAction

from deadept import DeAdept
from deadept.platform import PlatformSelector

selector = PlatformSelector()
parser = ArgumentParser()

def decode():
	parser.add_argument('-l', action=ListAction, help='List available platforms')
	parser.add_argument('-f', action='store_const', const=True, dest='force', help='Force writing of output to input file, this is here just to prevent accidental overwrites')
	parser.add_argument('-p', metavar='PLATFORM', type=str, dest='platform', choices=selector.platforms(), default=selector.default(), help=f'Platform to use for extracting the user key, the default is {selector.default()}')
	parser.add_argument('infile', type=str, help='Input epub file')
	parser.add_argument('outfile', type=str, default=None, nargs='?', help='(optional) output file')

	args = parser.parse_args()

	if not args.outfile and not args.force:
		print("Output filename not specified, use -f to just replace input file.")
		exit()

	da = DeAdept(args.infile, args.platform)
	da.decrypt(args.outfile)

def dump():
	parser.add_argument('-l', action=ListAction, help='List available platforms')
	parser.add_argument('-p', metavar='PLATFORM', type=str, dest='platform', choices=selector.platforms(), default=selector.default(), help=f'Platform to use for extracting the user key, the default is {selector.default()}')

	args = parser.parse_args()

	da = DeAdept(None, args.platform)
	key = da.getKey()

	with open('adept.der', 'bw') as fp:
		fp.write(key.export_key('DER'))

class ListAction(_HelpAction):
	def __call__(self, parser, namespace, values, option_string=None):
		print("Available platforms:\n")
		for platform in selector.platforms():
			print(platform)

		parser.exit()
