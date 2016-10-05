import getopt
import gitlab
import logging
import threading
import time
import sys

from peepingtom import Setup

class PeepingTom:

	def __init__(self, arguments):
		self.private_token = arguments.private_token
		self.project_id = arguments.project_id
		self.client = gitlab.Gitlab('http://gitlab.com', self.private_token)
		self.setup_mode = False
		self.setup = Setup(arguments.debug)
		logging.basicConfig(level=arguments.log_level)

	def fetch_build_status(self, project_id):
		latest_commit = self.client.project_commits.list(project_id=project_id, page=0, per_page=1)[0]
		latest_build = latest_commit.builds(page=0, per_page=1)[0];
		print(latest_build.status)

	def execute(self):
		threading.Thread(target=self.start_status_loop).start()
		threading.Thread(target=self.setup.await_input).start()
		while(1):
			time.sleep(1)

	# Fetch the project status every 30 seconds
	def start_status_loop(self):
		while (1):
			if self.setup.setup_mode is not True:
				self.fetch_build_status(self.project_id)
				time.sleep(5)

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
