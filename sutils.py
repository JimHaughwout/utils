"""SimpleApp.py"""

def getCount(logFile):
	import findspark
	findspark.init()

	from pyspark import SparkContext
	#logFile = "declaration.txt"  # Should be some file on your system
	sc = SparkContext("local", "Simple App")
	logData = sc.textFile(logFile).cache()

	numAs = logData.filter(lambda s: 'a' in s).count()
	numBs = logData.filter(lambda s: 'b' in s).count()
	answer = dict()
	answer['aCount'] = numAs
	answer['bCount'] = numBs
	sc.stop()

	import json
	return json.dumps(answer)
