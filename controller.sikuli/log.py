from sikuli.Sikuli import *
from datetime import *

class Log:
	dateformat = '%Y-%m-%d %H:%M:%S'
	timeformat = '%H:%M:%S'
	
	def __init__(self):
		now = datetime.now()
		self.info (now.strftime('Log started at ' + self.dateformat))
	
	def log(self, prefix, text):
		now = datetime.now()
		print ("["+prefix+"][" + now.strftime(self.timeformat) + "] >>> " + text)

	def info(self,text):
		self.log("log", text)

	def fail(self,text):
		text = text + "[" + path + "]"
		self.log("fail", text)
	
	def error(self,text):
		text = text + "[" + path + "]"
		self.log("error", text)
		