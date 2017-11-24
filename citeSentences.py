import xml.etree.ElementTree as ET
import re
import time
import os, csv
# from nltk.tokenize import sent_tokenize

rootDir = './data'
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
	print('Found directory: %s' % dirName)
	# for fname in fileList:
	# 	if( fname[-6:]=="_1.txt"):
	# 		print(dirName +"/"+ fname)
	# 		os.system("./ParsCit/bin/citeExtract.pl -m extract_all " + dirName + "/" + fname + " > " + dirName + "/" +"parsedData.xml")

	tree = ET.parse(dirName + "/parsedData.xml")
	root = tree.getroot()
	citationList = next(root.iter('citationList'))

	citationStrings = []
	for citation in citationList.iter('citation'):
		title = citation.find('title')
		booktitle = citation.find('booktitle')
		journal = citation.find('journal')
		if title != None: Onetitle = title.text
		elif booktitle!=None: Onetitle = booktitle.text
		elif journal!=None: Onetitle = journal.text
		else: Onetitle = "Title not found"
		Onetitle = Onetitle.strip()
		
		contexts = citation.find('contexts')
		if contexts==None: 			
			print("Reference without context:", Onetitle)
		else:            
			for context in contexts.findall('context'):
				citationStrings.append(context.attrib['citStr'])

	citeSentences = []
	for citation in citationList.iter('citation'):
		title = citation.find('title')
		booktitle = citation.find('booktitle')
		journal = citation.find('journal')
		if title != None: Onetitle = title.text
		elif booktitle!=None: Onetitle = booktitle.text
		elif journal!=None: Onetitle = journal.text
		else: Onetitle = "Title not found"
		Onetitle = Onetitle.strip()
		
		contexts = citation.find('contexts')
		if contexts==None: 			
			print("Reference without context:", Onetitle)
		else:
			for context in contexts.findall('context'):
				# citationStrings.append(context.attrib['citStr'])
				text = context.text
				for citationStr in citationStrings:
					print(citationStr)                    
					text = re.sub(r'\([ ,]*'+re.escape(citationStr)+'[ ,]*\)','CITATION', text)
					text = text.replace(citationStr, 'CITATION')
				sentences = text.split(". ")
				# sentences = sent_tokenize(text)
				# print(sentences)
				# time.sleep(1)
				citeSentences += filter(lambda sent: "CITATION" in sent, sentences)

	print (dirName)
	sys.exit()
	with open(dirName + "/citeSents.csv","w") as f:
		wr = csv.writer(f, delimiter="\n")
		citeSentences = list(set(citeSentences))
		for ele in citeSentences:
			wr.writerow([ele+",,"])
	print(citeSentences);


			
