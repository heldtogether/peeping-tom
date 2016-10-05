#!/usr/bin/python

import os, sys

from app import PeepingTom, PeepingTomArgs

def main(argv):
	args = PeepingTomArgs()
	args.parse_arguments(argv)

	app = PeepingTom(args)

	try:
		app.execute()
	except KeyboardInterrupt:
		os._exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
