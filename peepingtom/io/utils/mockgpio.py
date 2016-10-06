import select
import sys

class GPIO:

	BCM = None
	IN = None
	OUT = None

	@staticmethod
	def setmode(mode):
		pass

	@staticmethod
	def setup(pin, mode):
		pass

	@staticmethod
	def input(pin):
		i,o,e = select.select([sys.stdin],[],[],0.0001)
		for s in i:
			if s == sys.stdin:
				input = sys.stdin.readline()
				return True
			return False
