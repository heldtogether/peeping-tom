#!/usr/bin/python

import logging
import sys
import threading
import time

from arguments import PeepingTomArgs
from peepingtom import Fetch, Setup

def main(argv):
	args = PeepingTomArgs()
	args.parse_arguments(argv)

	logging.basicConfig(level=args.log_level)

	should_exit = threading.Event()
	setup = Setup(should_exit, args.debug)
	fetch = Fetch(should_exit, args.private_token, args.project_id)

	fetch.start()
	setup.start()

	try:
		while 1:
			time.sleep(1)
	except KeyboardInterrupt:
		should_exit.set()

if __name__ == "__main__":
   main(sys.argv[1:])
