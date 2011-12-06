from sikuli import *
import shutil
import os
from log import Log
from scenarioBase import ScenarioBase

class Lastfm(ScenarioBase):

	def __init__(self, log, variables):
		self.log = Log()
		self.variables = variables

	def firefoxIsOpenedState(self, args):
		path = args["Path"]
		self.log.info("Path to Firefox: "+path)
		self.closeFirefox(args)
		App.open(path)
		#wait Firefox to be started. Should be replaced by pretty "wait condition"
		wait(5)
		self.maximizeActiveWindow()

	def maximizeActiveWindow(self):
		if exists("Window_Maximize_Classic.png"):
			click("Window_Maximize_Classic.png")
		#Not implemented yet
		#if exists("Window_Maximize_Xp.png"):
		#	click("Window_Maximize_Xp.png")
		#Not implemented yet
		#if exists("Window_Maximize_Seven.png"):
		#	click("Window_Maximize_Seven.png")

	def closeFirefox(self, agrs):
		myApp = App("Firefox")
		myApp.close()

	def openLastFm(self, args):
		time = args["Time"]
		type("l", KEY_CTRL) # switch to address field
		self.set("www.last.fm")
		wait("Lastfm_logo.png", int(time))
		if self.mainPageOpened():
			self.log.info("Last Fm main page opened")
		else:
			self.log.info("Last Fm main page not opened in "+time+"seconds")

	def lastFmIsOpenedState(self, args):
		if not self.mainPageOpened():
			self.openLastFm()

	def foobar2000IsOpenedState(self, args):
		self.closeFoobar2000(args)
		self.openFoobar2000(args)

	def openFoobar2000(self, args):
		path = args["Path"]
		self.log.info("Path to foobar2000: "+path)
		self.closeFoobar2000(args)
		App.open(path)
		#wait foobar2000 to be started. Should be replaced by pretty "wait condition"
		wait(1)
		self.maximizeActiveWindow()

	def openMusicFile(self, args):
		path = args["Path"]
		self.openFileDialog(args)
		currentDir = os.getcwd()
		self.log.info("Current directory: "+currentDir)
		#TODO: Combine using build-in method
		fullPath = currentDir+"\\"+path
		self.set(fullPath)
		self.log.info("Music file is opened from: "+fullPath)

	def closeFoobar2000(self, args):
		myApp = App("foobar2000")
		myApp.close()

	def mainPageOpened(self):
		if exists("Lastfm_logo.png"):
			return True
		else:
			return False

	def loggedIn(self):
		if exists("Lastfm_inbox_logout.png"):
			return True
		else:
			return False

	def verifyIAmLoggedIn(self, args):
		if (self.loggedIn()==True):
			self.log.info("I'm logged in")
		else:
			self.log.error("I'm not logged in")
			return False

	def verifyICanSeeMainPage(self, args):
		if self.mainPageOpened():
			self.log.info("I can see main page")
		else:
			self.log.error("I can not see main page")
