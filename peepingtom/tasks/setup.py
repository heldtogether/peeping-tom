import bottle
import fileinput
import logging
import os
import shutil
from subprocess import call
import threading
import time

from admin.utils import Server
from admin.controllers import SetupController
from peepingtom.io import ResetButton

class Setup(threading.Thread):

	def __init__(self, should_exit, debug):
		threading.Thread.__init__(self)
		self.daemon = True
		self.should_exit = should_exit

		self.setup_mode = False
		self.debug = debug

		self.button = ResetButton()
		self.button.set_on_callback(self.toggle_setup)

		self.bottle = bottle.Bottle()
		self.server = Server(host='', port=8080)
		self.server.quiet = True
		self.__setup_routes()

		self.ssid = ''
		self.password = ''

	def run(self):
		self.button.start()
		while not self.should_exit.isSet():
			time.sleep(1)

	def toggle_setup(self):
		self.setup_mode = not self.setup_mode
		if self.setup_mode == True:
			self.__enter_setup()
		else:
			self.__exit_setup()

	def __enter_setup(self):
		logging.info('Entering setup.')
		self.__create_adhoc_network()
		self.__start_server()

	def __exit_setup(self):
		logging.info('Exiting setup.')
		self.__create_default_network()
		self.__stop_server()

	def __create_default_network(self):
		source = os.path.dirname(__file__) + "/../templates/wifi/default.conf"
		target = "/etc/network/interfaces"
		logging.info('Switching network configuration at %s for %s.', target, source)
		if (self.debug is not True):
			shutil.copy(source, target)
			for line in fileinput.input(source, inplace=True):
				print line.replace("{{ssid}}", self.ssid),
			for line in fileinput.input(source, inplace=True):
				print line.replace("{{password}}", self.password),
			call(["dhclient", "wlan0"])

	def __create_adhoc_network(self):
		source = os.path.dirname(__file__) + "/../templates/wifi/adhoc.conf"
		target = "/etc/network/interfaces"
		logging.info('Switching network configuration at %s for %s.', target, source)
		if (self.debug is not True):
			shutil.copy(source, target)
			call(["dhclient", "wlan0"])

	def __start_server(self):
		logging.info("Starting server.")
		thread = threading.Thread(target=self.bottle.run, kwargs={'server': self.server})
		thread.daemon = True
		thread.start()

	def __stop_server(self):
		logging.info("Stopping server.")
		self.server.stop()

	def __callback(self, ssid, password):
		self.ssid = ssid
		self.password = password

	def __setup_routes(self):
		setup_controller = SetupController(self.__callback)
		self.bottle.route('/', 'GET', setup_controller.index)
		self.bottle.route('/', 'POST', setup_controller.save)
