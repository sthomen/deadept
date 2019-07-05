from argparse import ArgumentParser

from deadept import DeAdept

def run():
	parser = ArgumentParser()
	parser.add_argument('infile', type=str, help='Input epub file')
	parser.add_argument('outfile', type=str, default=None, nargs='?', help='(optional) output file')
	parser.add_argument('-p', metavar='PLATFORM', type=str, dest='platform', default='Windows', help='Platform to use for extracting the user key, the default is Windows')
	parser.add_argument('-f', type=bool, dest='force', help='Force writing of output to input file, this is here just to prevent accidental overwrites')

	args = parser.parse_args()

	if not args.outfile and not args.force:
		print("Output filename not specified, use -f to just replace input file.")
		exit()

	da = DeAdept(args.infile, args.platform)
	da.decrypt(args.outfile)
