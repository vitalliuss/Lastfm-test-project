from sikuli import *
from log import Log

class Tests:

	def __init__(self):
		self.log = Log()

	def setUp(self):
		# using an existing window if possible
		myApp = App("Firefox")
		myApp.close()
		wait(1)
		App.open("c:\\Program Files (x86)\\Mozilla Firefox\\Firefox.exe")
		wait(2)
		type("l", KEY_CTRL) # switch to address field
		type("www.last.fm")
		type(Key.ENTER)
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

	def runAllTests(self):
		self.log.info("Running all tests ...")
		self.setUp()
		self.ICanSeeMainPage()
		self.IAmLoggedIn()

	def IAmLoggedIn(self):
		if (self.loggedIn()==True):
			self.log.info("I'm logged in")
			return True
		else:
			self.log.info("I'm not logged in")
			return False

	def ICanSeeMainPage(self):
		if exists("Lastfm_logo.png"):
			self.log.info("I can see main page")
			return True
		else:
			self.log.info("I can see main page")
			return False
