from log import Log
from sikuli.Sikuli import *
from datetime import *
import time

class ScenarioBase(object):

	def __init__(self, log, variables):
		self.log = log
		self.variables = variables
		
	def getInfo(self, args):
		self.log.info("Parameters passed to step:")
		info = args["info"]
		info = "," + info[0 : len(info) - 1]
		infoItems = {}
		while info != "":
			leninfo = len(info)
			equalPosition = len(info) - 1 - info[::-1].find("=")
			value = info[equalPosition + 1 : len(info)]
			info = info[0 : equalPosition]
			commaPosition = len(info) - 1 - info[::-1].find(",")
			key = info[commaPosition + 1 : len(info)]
			info = info[0 : commaPosition]
			infoItems[key] = value
			if len(info) == leninfo:
				break
		return infoItems	

	def readLine(self, filename, text):
		count = 0
		self.log.info("Search for "+text)
		file = open(filename)
		for line in file.readlines(count):
			if line.find(text)>-1:
				newline= line.rsplit("\n")[0]
				self.log.info("Founded: ["+newline+"] line")
				self.log.info("Line # "+str(count+1))
				return newline
			else:
				pass	
			count = count + 1

	def setAndGoToNext(self, value):
		type(value)
		type(Key.ENTER)
		type(Key.TAB)
	
	def set(self, value):
		type(value)
		type(Key.ENTER)	
		
	def getClipboardText(self):
		type("a", KEY_CTRL)
		type("c", KEY_CTRL)
		data = Env.getClipboard()
		return data
	
	def getData(self):
		#TODO: send CTRL+C key
		time.sleep(1)
		return self.getClipboardText()
		
	def waitUserAction(self, message):
		popup(message)
		wait(3)
		
	def openFileDialog(self, args):
		type("o", KEY_CTRL)
		self.log.info("Open file dialog is opened")
		wait(1)
	