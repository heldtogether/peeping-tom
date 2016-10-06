#!/usr/bin/python

import logging
import sys
import threading
import time

from peepingtom import Arguments, tasks

def main(argv):
	args = Arguments()
	args.parse_arguments(argv)

	logging.basicConfig(level=args.log_level)

	should_exit = threading.Event()
	setup = tasks.Setup(should_exit, args.debug)
	fetch = tasks.Fetch(should_exit, args.private_token, args.project_id)

	fetch.start()
	setup.start()

	try:
		while 1:
			time.sleep(1)
	except KeyboardInterrupt:
		should_exit.set()

if __name__ == "__main__":
   main(sys.argv[1:])
