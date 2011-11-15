from sikuli.Sikuli import *
from datetime import *
from controller import *
import shutil
import os

class Log:
	errorOccured = False
	failed = False
	reason = ""	
	dateformat = '%Y-%m-%d %H:%M:%S'
	timeformat = '%H:%M:%S'
	screenshotTimeFormat = '%H-%M-%S'
	pauseOnFailFlag = False
	
	def __init__(self):
		self.errorOccured = False
		self.failed = False
		self.reason = ""
		now = datetime.now()
		self.info (now.strftime('Log started at ' + self.dateformat))
	
	def log(self, prefix, text):
		now = datetime.now()
		print ("["+prefix+"][" + now.strftime(self.timeformat) + "] >>> " + text)

	def info(self,text):
		self.log("log", text)

	def fail(self,text):
		path = self.createScreenshot("default", "default")
		text = text + "[" + path + "]"
		self.log("fail", text)
		self.finishFail(text)
	
	def error(self,text):
		path = self.createScreenshot("default", "default")
		text = text + "[" + path + "]"
		self.log("error", text)
		self.errorOccured = True
		self.finishFail(text)
	
	def finishFail(self, text):
		if not self.failed:
			self.failed = True
			self.reason = text
		if (self.pauseOnFailFlag):
			self.askUser()

	def comment(self, text):
		#logging comment to TestResultSummary
		if(self.testResults):
			self.testResults.appendComment(text);
		self.info(text)

	def clearFail(self):
		self.errorOccured = False
		self.failed = False
		self.reason = ""	
		
	def createScreenshot(self, name, directory):
		now = datetime.now()
		time = now.strftime(self.screenshotTimeFormat)
		if (name == "default"):
			name = time
		if (directory == "default"):
			directory = "Screenshots"	
		try:
			os.mkdir(directory)
		except OSError:
			pass
		destination = str(directory)+"\\"
		name = str(name) + ".png"
		f = capture(getBounds())
		shutil.move(f, destination + name)
		path = destination + name
		self.info("Screenshot saved: " + destination + name)
		return path	
		
	def askUser(self):
		self.info("Script was paused. Waiting for user action...")
		action = input("Script was paused due some issues\nType 'stop' to stop the script or click OK to continue:")
		if (action == "stop"):
			self.info("Script will stop now by user decision")
			exit(1) #script will exit with code "1"
		else:
			self.info("Script will resume working in 3 seconds")
			wait(3)
			
	def pauseOnFail(self, value):
		self.info("Setting pauseOnFailFlag to " + str(value))
		self.pauseOnFailFlag = False
		try:
			if (value == "True"):
				self.pauseOnFailFlag = True
		except ValueError:
			wait(0)
			# do nothing
			