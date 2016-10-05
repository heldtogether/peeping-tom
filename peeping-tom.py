#!/usr/bin/python

import sys

from app import PeepingTom, PeepingTomArgs

def main(argv):
	args = PeepingTomArgs()
	args.parse_arguments(argv)

	app = PeepingTom(args)
	app.execute()

if __name__ == "__main__":
   main(sys.argv[1:])
