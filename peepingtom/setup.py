import bottle
import logging
import os
import shutil
from subprocess import call
import threading
import time

from admin.utils import Server
from admin.controllers import SetupController

class Setup:

	def __init__(self, debug):
		self.setup_mode = False
		self.debug = debug
		self.bottle = bottle.Bottle()
		self.server = Server(host='localhost', port=8080)
		self.server.quiet = True
		self.__setup_routes()

	# Listen out for input. This will be replaced
	# by GPIO input'
	def await_input(self):
		# Start the app as though it's
		# already set up. Have the user
		# choose to configure it.
		self.__exit_setup()
		while(1):
			s = raw_input()
			self.setup_mode = not self.setup_mode
			if self.setup_mode == True:
				self.__enter_setup()
			else:
				self.__exit_setup()
			time.sleep(1)

	def __enter_setup(self):
		logging.info('Entering setup.')
		self.__create_adhoc_network()
		self.__start_server()

	def __exit_setup(self):
		logging.info('Exiting setup.')
		self.__create_default_network()
		self.__stop_server()

	def __create_default_network(self):
		source = os.path.dirname(__file__) + "/wifi-config/default.conf"
		target = "/etc/network/interfaces"
		logging.info('Switching network configuration at %s for %s.', target, source)
		if (self.debug is not True):
			shutil.copy(source, target)
			call(["dhclient", "wlan0"])

	def __create_adhoc_network(self):
		source = os.path.dirname(__file__) + "/wifi-config/adhoc.conf"
		target = "/etc/network/interfaces"
		logging.info('Switching network configuration at %s for %s.', target, source)
		if (self.debug is not True):
			shutil.copy(source, target)
			call(["dhclient", "wlan0"])

	def __start_server(self):
		logging.info("Starting server.")
		threading.Thread(target=self.bottle.run, kwargs={'server': self.server}).start()

	def __stop_server(self):
		logging.info("Stopping server.")
		self.server.stop()

	def __setup_routes(self):
		setup_controller = SetupController()
		self.bottle.route('/', 'GET', setup_controller.index)
