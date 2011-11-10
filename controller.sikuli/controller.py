from log import Log
from tests import Tests
from sikuli import *

class Controller:
		
	def __init__(self):
		self.log = Log()
		self.tests = Tests()
				
	def run(self):
		self.log.info("Test start")
		self.runTests()

	def runTests(self):
		self.log.info("All tests is starting")
		self.tests.runAllTests()
		self.log.info("All tests is finished")