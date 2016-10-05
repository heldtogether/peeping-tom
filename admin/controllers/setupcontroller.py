import os

from bottle import static_file, request

class SetupController:

	def __init__(self, callback):
		self.callback = callback

	def index(self):
		return static_file('index.html', root=os.path.dirname(__file__) + '/../views')

	def save(self):
		ssid = request.forms.get('ssid')
		password = request.forms.get('password')
		self.callback(ssid, password)
		return static_file('saved.html', root=os.path.dirname(__file__) + '/../views')
