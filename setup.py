import logging
import os
from subprocess import call
import time

class Setup:

	def __init__(self, debug):
		self.setup_mode = True
		self.debug = debug

	# Listen out for input. This will be replaced
	# by GPIO input'
	def await_input(self):
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

	def __exit_setup(self):
		logging.info('Exiting setup.')
		self.__create_default_network()

	def __create_default_network(self):
		source = os.getcwd() + "/wifi-config/default.conf"
		target = "/etc/networks/interfaces"
		logging.info('Switching network configuration at %s for %s.', target, source)
		if (self.debug is not True):
			os.symlink(source, target)
			call(["dhclient", "wlan0"])

	def __create_adhoc_network(self):
		source = os.getcwd() + "/wifi-config/adhoc.conf"
		target = "/etc/networks/interfaces"
		logging.info('Switching network configuration at %s for %s.', target, source)
		if (self.debug is not True):
			os.symlink(source, target)
			call(["dhclient", "wlan0"])
