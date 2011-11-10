from sikuli.Sikuli import *
from log import Log

class Tests:

	def __init__(self):
		self.log = Log()

	def runAllTests(self):
		self.log.info("Running all tests ...")
		self.firstTest()
		self.secondTest()

	def firstTest(self):
		self.log.info("Running test #1 ...")

	def secondTest(self):
		self.log.info("Running test #2 ...")		

