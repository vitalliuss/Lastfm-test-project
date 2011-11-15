class ExecutionList:
	def __init__(self, inputDir):
		filename = "ExecutionList.txt"
		self.fullFilename = inputDir + filename;
	def getDelimeter(self):
		return '\t'
	def readLines(self):
		executionList = file(self.fullFilename, "r")
		lines = executionList.readlines()
		executionList.close()
		return lines
