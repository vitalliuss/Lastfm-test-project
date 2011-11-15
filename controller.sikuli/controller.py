from executionList import ExecutionList
from log import Log
from testResults import TestResults
from sikuli.Sikuli import *

class Controller:
		
	def __init__(self):
		self.log = Log()
		inputDir = ""
		outputDir = inputDir
		testResultsSummaryFile = "TestResultsSummary.txt"
		self.fullTestResultsSummaryFileName = outputDir + testResultsSummaryFile
		self.executionList = ExecutionList(inputDir)
		self.variables = {}
		self.applications = {}
		
	def run(self):
		self.log.info("Test start")
		self.processExecutionList()
		
	def processExecutionList(self):
		lines = self.executionList.readLines()
		keywordIndex = 0
		testResults = TestResults(self.fullTestResultsSummaryFileName, lines)
		self.log.testResults = testResults
		for line in lines:
			items = self.parseExecutionLine(line)
			keyword = items[keywordIndex]
			if keyword == "TestScenario" or keyword == "TestGroup" or keyword == "TestCase":
				result = testResults.endTestCase(self.log.failed, self.log.reason)
				if result != "":
					self.log.info("Test case status: " + result)
				self.log.clearFail()
			if keyword == "TestScenario" or keyword == "TestGroup":
				self.log.info(keyword + ": " + items[1])
			elif keyword == "TestCase":
				self.log.info("==================================================");
				self.log.info("TestCase: [" + items[2] + "] " + items[1]);
				testResults.startTestCase()
			elif keyword == "Assign":
				items[2] = self.replaceVariables(items[2])
				if items[2].find("=") == 0:
					logMessage = "Assign: " + items[1] + items[2]
				else:
					logMessage = "Assign: " + items[1] + "=" + items[2]
				if self.log.errorOccured and items[6].find("Don't skip") == -1:
					self.log.info("Skip: " + logMessage)
				else:
					self.log.info(logMessage)
					self.assignVariable(items[1], items[2])
			else:
				params = items[1 : 6]
				for i in range(5):
					params[i] = self.replaceVariables(params[i])
				logMessage = keyword + "(" + str(params).replace(", ''", "") + ")"
				if self.log.errorOccured and items[6].find("Don't skip") == -1:
					self.log.info("Skip: " + logMessage)
				else:
					self.log.info(logMessage)
					self.runStep(keyword, params)
		result = testResults.endTestCase(self.log.failed, self.log.reason)
		if result != "":
			self.log.info("Test case status: " + result)

	def parseExecutionLine(self, line):
		""" takes execution line and returns fields as array, with all necessary transformations"""
		items = line.split(self.executionList.getDelimeter())
		for i in range(len(items)):
			items[i] = self.unquote(items[i])
		return items
	
	def replaceVariables(self, expression):
		try:
			resultExpression = ""
			addToResult = True
			varName = ""
			for currentChar in expression:
				if currentChar == '{':
					addToResult = False
				if addToResult:
					resultExpression = resultExpression + currentChar
				else:
					varName = varName + currentChar
				if currentChar == '}':
					addToResult = True
					if len(varName) > 2:
						if self.variables.has_key(varName[1 : len(varName) - 1]):
							varName = self.variables[varName[1 : len(varName) - 1]]
					resultExpression = resultExpression + varName
					varName = ""
			return resultExpression
		except:
			return expression

	def addApplication(self, appName):
		if not self.applications.has_key(appName):
			exec("from " + appName.lower() + " import " + appName)
			exec("self.applications[appName] = " + appName + "(self.log, self.variables)")
	
	def assignVariable(self, varName, expression):
		self.variables.pop(varName, "")
		if expression.find("=") == 0:
			try:
				args = {}
				pointPosition = expression.find(".")
				bracketPosition = expression.find("(")
				appName = expression[1 : pointPosition]
				methodName = expression[pointPosition + 1 : bracketPosition]
				methodName = methodName[0 : 1].lower() + methodName[1 : len(methodName)]
				argsString = expression[bracketPosition + 1 : len(expression) - 1]
				self.addApplication(appName)
				if argsString != "":
					for pairString in argsString.split(","):
						pair = pairString.split("=")
						args[pair[0]] = pair[1]
				exec("result = self.applications[appName]." + methodName + "(args)")
				self.variables[varName] = result
			except BaseException, e:
				self.log.error(str(e))
			except FindFailed, e:
				self.log.error(str(e))
		else:
			self.variables[varName] = expression
			self.processSpecialVariables(varName, expression)
			
	def unquote(self, expression):
		""" if from both sides there are " (double-quote), they are removed,
		and all "" (2 double-quotes) inside of variable are substituded to " (1 double-quote) """
		if (expression.find('"') == 0):
			while ((expression[0] == '"') and (expression[len(expression) - 1] == '"')):
				expression = expression[1 : len(expression) - 1]
				expression = expression.replace('""', '"')
		return expression
	
	def processSpecialVariables(self, varName, varValue):
		self.log.info("Process special variable: "+varName +" "+varValue)
		try:
			dictionary = {
				"PauseOnFail": self.log.pauseOnFail };
			function = dictionary[varName]
		except KeyError:
			function = None
		if (function!=None):
			self.log.info(varName + " is special variable")
			function(varValue)
		else:
			self.log.info(varName + " is NOT special variable")
			
	def runStep(self, stepName, params):
		try:
			appName = stepName.split(".")[0]
			self.addApplication(appName)
			methodName = stepName.split(".")[1]
			methodName = methodName[0 : 1].lower() + methodName[1 : len(methodName)]
			args = {}
			for pairString in params:
				if pairString == "":
					break
				equalPosition = pairString.find("=")
				args[pairString[0 : equalPosition]] = pairString[equalPosition + 1 : len(pairString)]
			exec("self.applications[appName]." + methodName + "(args)")
		except BaseException, e:
			self.log.error(str(e))
		except FindFailed, e:
				self.log.error(str(e))

			