import os
 
rootDir = './data'
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
	print('Found directory: %s' % dirName)
	for fname in fileList:
		if( fname[-6:]=="_1.txt"):
			print(dirName +"/"+ fname)
			os.system("./ParsCit/bin/citeExtract.pl -m extract_all " + dirName + "/" + fname + " > " + dirName + "/" +"parsedData.xml")