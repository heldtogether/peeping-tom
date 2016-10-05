import getopt
import logging
import threading
import time
import sys

from peepingtom import Fetch, Setup

class PeepingTom:

	def __init__(self, arguments):
		self.setup = Setup(arguments.debug)
		self.fetch = Fetch(arguments.private_token, arguments.project_id)
		logging.basicConfig(level=arguments.log_level)

	def execute(self):
		threading.Thread(target=self.fetch.fetch_build_status).start()
		threading.Thread(target=self.setup.await_input).start()
		while(1):
			time.sleep(1)

class PeepingTomArgs:

	def __init__(self):
		self.private_token = ''
		self.project_id = ''
		self.log_level = logging.WARN
		self.debug = False

	def parse_arguments(self, argv):
		try:
			opts, args = getopt.getopt(argv, "ht:p:",["log=", "debug"])
		except getopt.GetoptError:
			self.display_help()
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				self.display_help()
				sys.exit()
			elif opt in ("-t"):
				self.private_token = arg
			elif opt in ("-p"):
				self.project_id = arg
			elif opt in ("--log"):
				self.log_level = getattr(logging, arg.upper())
			elif opt in ("--debug"):
				self.debug = True

		if self.private_token == '' or self.project_id == '':
			self.display_help()
			sys.exit(2)

	def display_help(self):
		print 'peeping-tom.py -t <private-token> -p <project_id>'
