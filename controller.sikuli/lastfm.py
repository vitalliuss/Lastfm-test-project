from sikuli import *
import shutil
import os
from log import Log
from scenarioBase import ScenarioBase

class Lastfm(ScenarioBase):
	
	mainPage = "www.last.fm"
	loginPage = "https://www.last.fm/login"
	logoutPage = "http://www.lastfm.ru/login/logout"
	userPage = "http://www.lastfm.ru/user/vitalliuss"
	#Set find failedd response to "SKIP". FindFailed exception will not raise any more.
	setFindFailedResponse(SKIP)

	def __init__(self, log, variables):
		self.log = Log()
		self.variables = variables

	def firefoxIsOpenedState(self, args):
		if not exists("Mozilla Firefox"):
			path = args["Path"]
			self.log.info("Path to Firefox: "+path)
			self.closeFirefox(args)
			App.open(path)
			#wait Firefox to be started. Should be replaced by pretty "wait condition"
			wait(5)
			self.maximizeActiveWindow()
			self.log.info("Firefox is opened")
		else:
			self.log.info("Firefox is already opened")

	def maximizeActiveWindow(self):
		if exists("Window_Maximize_Classic.png"):
			click("Window_Maximize_Classic.png")
		#Not implemented yet
		#if exists("Window_Maximize_Xp.png"):
		#	click("Window_Maximize_Xp.png")
		elif exists("Window_Maximize_Seven.png"):
			click("Window_Maximize_Seven.png")

	def closeFirefox(self, agrs):
		myApp = App("Firefox")
		myApp.close()

	def openLastFm(self, args):
		time = args["Time"]
		self.openPage(self.mainPage)
		#find failed
		wait(int(time))
		if self.mainPageOpened():
			self.log.info("Last Fm main page opened")
		else:
			self.log.info("Last Fm main page not opened in "+time+"seconds")

	def lastFmIsOpenedState(self, args):
		if not self.mainPageOpened():
			self.firefoxIsOpenedState(args)
			self.openLastFm(args)

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
		if exists("Foobar2000_crash_report.png"):
			#Select option "Start normally"
			type(Key.DOWN)
			type(Key.DOWN)
			type(Key.ENTER)
			wait(1)
		self.maximizeActiveWindow()
		
	def verifyFoobar2000IsOpened(self, args):
		if exists("Foobar2000_buttons.png"):
			return True
			self.log.info("Foobar2000 is opened")
		else:
			return False
			self.log.error("Foobar2000 is not opened")

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
		elif exists("Lastfm_logo_2.png"):
			return True
		else:
			return False

	def loggedIn(self):
		if exists("Lastfm_inbox_logout.png"):
			return True
		elif exists("Lastfm_inbox_logout_rus.png"):
			return True
		else:
			return False
			
	def logIn(self, args):
		#TODO: Make it work
		time = args["Time"]
		login = args["Login"]
		password = args["Password"]
		if not self.loggedIn():
			self.openPage(self.loginPage)
			wait("Login_label.png", int(time))
			type("a", KEY_CTRL)
			type(Key.DELETE)
			type(login)
			type(Key.TAB)
			type(password)
			type(Key.ENTER)
		else:
			return True
		
	def logOut(self, args):
		time = args["Time"]
		if self.loggedIn():
			self.openPage(self.logoutPage)
			wait("Logout_button.png", int(time))
			click("Logout_button.png")
		else:
			return True
		
	def openUserPage(self, args):
		if not self.userPageIsOpened():
			self.openPage(self.userPage)
		else:
			pass
		self.log.info("User page is opened")	
		
	def userPageIsOpened(self):
		if exists("User_pic.png"):
			return True
		else:
			return False

	def verifyICanSeeUserPage(self, args):
		if self.userPageIsOpened():
			self.log.info("I can see user page")
			return True
		else:
			self.log.error("I cannot see user page")
			return False
		
	def verifyIAmScrobblingNowFromFoobar2000(self, args):
		if exists("Scrobbling_now_from_foobar2000.png"):
			self.log.info("I'm scrobbling from foobar2000")
			return True
		else:
			self.log.error("I'm not scrobbling from foobar2000")
			return False
		
	def verifyIAmListeningNow(self, args):
		if exists("Listening_now.png"):
			self.log.info("I'm listening now")
			return True
		else:
			self.log.error("I'm not listening now")
			return False
			
	def verifyArtistNameAndSong(self, args):
		artist = args["Artist"]
		song = args["Song"]
		searchPattern = artist+" - "+song
		self.log.info("Searching for: "+searchPattern)
		if exists(searchPattern):
			self.log.info("Artist and song are valid")
			return True
		else:
			self.log.error("Artist and song are invalid")
			return False
		
	def verifyIAmLoggedIn(self, args):
		if self.loggedIn():
			self.log.info("I'm logged in")
		else:
			self.log.error("I'm not logged in")
	
	def verifyIAmLoggedOut(self, args):
		if not self.loggedIn():
			self.log.info("I'm logged out")
		else:
			self.log.error("I'm not logged out")

	def verifyICanSeeMainPage(self, args):
		if self.mainPageOpened():
			self.log.info("I can see main page")
		else:
			self.log.error("I can not see main page")
