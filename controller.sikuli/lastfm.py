from sikuli import *
from log import Log
from scenarioBase import ScenarioBase

class Lastfm(ScenarioBase):

	def __init__(self, log, variables):
		self.log = Log()
		self.variables = variables

	def firefoxIsOpenState(self, args):
		self.closeFirefox(args)
		App.open("c:\\Program Files (x86)\\Mozilla Firefox\\Firefox.exe")
		#wait Firefox to be started. Should be replaced by pretty "wait condition"
		wait(5)
		
	def closeFirefox(self, agrs):
		myApp = App("Firefox")
		myApp.close()
		
	def openLastFm(self, args):	
		type("l", KEY_CTRL) # switch to address field
		self.set("www.last.fm")
		wait("Lastfm_logo.png", 10)
		if exists("Lastfm_logo.png"):
			self.log.info("Last Fm main page opened")
		else:
			self.log.info("Last Fm main page not opened in 10 seconds")

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
		if exists("Lastfm_logo.png"):
			self.log.info("I can see main page")
		else:
			self.log.error("I can not see main page")
