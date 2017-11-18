import xml.etree.ElementTree as ET
import re
import sys
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import operator 
from collections import defaultdict
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

# print files

totalCitations = defaultdict(int)
steps = 0
MaxSteps = 5
totCit = 0
title_to_id = defaultdict(str)
allSections = set()
debug_title = 'J01-3003'
#expreiment, intro, related work, discussion, conclusion, results, future work
titleAbsent = set()

for file in files:
	try:
		tree = ET.parse(file[0])
		root = tree.getroot()
		paperTitle = root[1][0].find('title')
		if paperTitle==None:
			pass
			# print "Title not found:",file[0]
		else:
			stemmed = [ps.stem(word) for word in paperTitle.text.split()]
			paperTitle = " ".join(stemmed)
			paperTitle = paperTitle.lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")
			# print paperTitle
			title_to_id[paperTitle] = file[0][5:13]

		if paperTitle==None:
			titleAbsent.add(file[0][5:13])
		if file[0][5:13] == debug_title or file[0][5:13] == 'xxx': print (paperTitle)
	except:
		pass

fp = open('db/MeaningfulCitationsDataset/ValenzuelaAnnotations.csv', 'r')

dataset = set()
citedPapers = set()

feature1 = defaultdict(int)
totalCitations = defaultdict(int)
sectionCount = {}

x=0
y=0

sectionList = ["experiment", "introduction", "related work", "discussion", "conclusion", "results", "future work", "other"]

fp.readline()

for line in fp:
	data = line.split(',')
	# print data
	citedPapers.add(data[1])
	dataset.add((data[1], data[2]))
	sectionCount[(data[1], data[2])]={}
	for xx in sectionList:
		sectionCount[(data[1], data[2])][xx]={}




def addSection(paperID, citationID, section):
	if section!="": return
	if (citationID, paperID) in dataset:
		for sec in sectionList:
			if sec in section:
				sectionCount[(citationID, paperID)][sec]+=1
		else:
			sectionCount[(citationID, paperID)]["other"]+=1


for file in files:
	# if steps > MaxSteps: break	#comment this
	try:
		tree = ET.parse(file[0])
		root = tree.getroot()
		paperTitle = root[1][0].find('title')
		if paperTitle == None: paperTitle = ""
		else:
			stemmed = [ps.stem(word) for word in paperTitle.text.split()]
			paperTitle = " ".join(stemmed)
			paperTitle = paperTitle.lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")
			# if paperTitle[:2] == 'b\'': paperTitle = paperTitle[2:]


		# print file[0]
		tree = ET.parse(file[0])
		root = tree.getroot()
		citationList = next(root.iter('citationList'))
		totCit += len(citationList)
		if title_to_id[paperTitle] == debug_title:
			print ("starting")

		i=0
		for citation in citationList:


			
			title = citation.find('title')
			booktitle = citation.find('booktitle')
			journal = citation.find('journal')
			if title != None: Onetitle = title.text
			elif booktitle!=None: Onetitle = booktitle.text
			elif journal!=None: Onetitle = journal.text
			else: Onetitle = ""
			stemmed = [ps.stem(word) for word in Onetitle.text.split()]
			Onetitle = " ".join(stemmed)
			Onetitle = Onetitle.lstrip().rstrip().lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")

			paperID = None
			citationID = None
			for xx in title_to_id:
				if (paperTitle in xx) :
					paperID = title_to_id[xx]

			for xx in title_to_id:
				if ((Onetitle in xx) or (xx in Onetitle)) and (Onetitle != '') and (xx != ''):
					citationID = title_to_id[xx]


			if paperID == debug_title:
				print ((Onetitle, citationID))


			if citationID and paperID:
				pass
				# print title_to_id[paperTitle], paperTitle, '#', title_to_id[Onetitle], Onetitle
				
			# if citationID not in citedPapers: #no need to look at this citation
			# 	continue 
			if (citationID, paperID) in dataset:
				y+=1
				dataset.remove((citationID, paperID))
				# print title_to_id[paperTitle], paperTitle, '#', title_to_id[Onetitle], Onetitle




			contexts = citation.find('contexts')
			if contexts==None: 
				# totalCitations[citationID] += 1
				# feature1[(citationID, paperID)] += 1
				pass
				# print "Reference without context:", Onetitle
			else:
				totalCitations[citationID] += len(contexts.findall('context'))
				feature1[(citationID, paperID)] += len(contexts.findall('context'))
				# print Onetitle, len(contexts.findall('context')), totalCitations[Onetitle]
				for context in contexts.findall('context'):
					steps += 1
					SectLabel = root[0][0]	#0 is SectLabel, variant 0
					curSection = ""
					ans = ""
					alltext = ""
					for child in SectLabel:
						if child.text!=None: alltext+=child.text
						if child.tag == 'sectionHeader': 
							curSection = child.text
							allSections.add(curSection.rstrip().lstrip().lower() + " : " + file[0] )
						# elif child.tag == 'bodyText':
						# 	# if child.get('confidence')=='0.953295307692308': print re.sub(r'[- \n\s]*','',alltext), "\nOVER\n", re.sub(r'[- \n\s]*','',context.text)
						# 	if re.sub(r'[- \n\s\t]*','',alltext).lower().find(re.sub(r'[- \n\s\t]*','',context.text).lower())!=-1:
						# 		#print Onetitle, curSection
						# 		curSection = curSection.rstrip().lstrip()
						# 		result = ''.join(i for i in curSection if not i.isdigit())
						# 		result.lstrip().rstrip()
						# 		addSection(paperID, citationID, result)
						# 		ans = result
						# 		allSections.add(result)
						# 		break

					#if ans == "": print "Not found", Onetitle
	except:
		pass
# print "citaion, cited by, # direct citations, experiment, introduction, related work, discussion, conclusion, results, future work, other, f8"
# for xx in dataset2:
# 	print xx[0], ',', xx[1], ','
# 	print feature1[xx], ','
# 	for sec in sectionCount: print sectionCount[xx][sec], ','
# 	if totalCitations[xx[0]]!=0:
# 		print feature1[xx]*1.0/totalCitations[xx[0]]
# 	else: print xx[0]
# 	print '\n'


# totalCitations = dict(totalCitations)
# topCited = sorted(totalCitations.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
# print topCited, len(totalCitations), totCit

# for xx in dataset.copy():
# 	if xx[0] in titleAbsent or xx[1] in titleAbsent:
# 		dataset.remove(xx)
# print (dataset)
print ((x,y))

# f1 = open("allSections.txt", "wb")
# for x in allSections: 
# 	f1.write(x+"\n")
# b using predicate argument structures for information extraction
# using predicate arguments structures for information extraction
