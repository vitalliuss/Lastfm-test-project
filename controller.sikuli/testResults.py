from datetime import *
from log import Log

class TestResults:
	results = []
	currentTestCase = -1
	start = None
	resultsFileName = ""
	testCaseStarted = False

	def __init__(self, resultsFileName, lines):
		self.testCaseStarted = False
		self.resultsFileName = resultsFileName
		self.currentTestCase = -1
		self.results = []
		for line in lines:
			if line.find("TestCase\t") == 0:
				fields = line.split("\t")
				self.results.append(self.getTestCaseInitialInfo(fields[2], fields[1], fields[6]))
		self.saveResults()

	def getTestCaseInitialInfo(self, testCaseID, description, comment):
		result = {}
		result["testCaseID"] = testCaseID;
		result["description"] = description;
		result["status"] = "Not executed";
		result["comment"] = comment;
		result["details"] = "";
		result["executionTime"] = timedelta(0);
		return result

	def startTestCase(self):
		self.start = datetime.now()
		self.currentTestCase = self.currentTestCase + 1
		self.testCaseStarted = True

	def endTestCase(self, failed, reason):
		if not self.testCaseStarted:
			return ""
		self.testCaseStarted = False
		if failed:
			self.results[self.currentTestCase]["status"] = "Failed"
			self.results[self.currentTestCase]["details"] = reason
		else:
			self.results[self.currentTestCase]["status"] = "Passed"
		self.results[self.currentTestCase]["executionTime"] = datetime.now() - self.start
		self.saveResults()
		return self.results[self.currentTestCase]["status"]
		
	def appendComment(self, comment):
		self.results[self.currentTestCase]["comment"] += comment

	def saveResults(self):
		header = "Test Case ID	Description	Status	Comment	Details	Execution Time"
		eol = '\n'
		trs=file(self.resultsFileName, "w")
		trs.write(header+eol)
		for result in self.results:
			resultStr = ""
			resultStr = result["testCaseID"] + "\t" + result["description"] + "\t" + result["status"] + "\t" + result["comment"] + "\t" + result["details"] + "\t" + str(result["executionTime"])
			resultStr = resultStr.replace("\r\n", " ")
			resultStr = resultStr.replace("\n\r", " ")
			resultStr = resultStr.replace("\r", " ")
			resultStr = resultStr.replace("\n", " ")
			resultStr = resultStr + eol
			trs.write(resultStr)
		trs.flush()
		trs.close





