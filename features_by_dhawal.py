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
<<<<<<< HEAD
=======

>>>>>>> fe9acd6518025ad1138b0ecfab6d95b6f8094c2c
ps = PorterStemmer()

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

# print files

totalCitations = defaultdict(int)
steps = 0
MaxSteps = 50
totCit = 0
title_to_id = defaultdict(str)
allSections = set()
debug_title = 'W09-2501'
#expreiment, intro, related work, discussion, conclusion, results, future work
titleAbsent = set()

for file in files:
<<<<<<< HEAD
	tree = ET.parse(file[0])
	root = tree.getroot()
	paperTitle = root[1][0].find('title')
	if paperTitle==None:
		pass
		# print "Title not found:",file[0]
	else:
		paperTitle = paperTitle.text.lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")
		# print paperTitle
		title_to_id[paperTitle] = file[0][5:13]

	if paperTitle==None:
		titleAbsent.add(file[0][5:13])
	if file[0][5:13] == debug_title or file[0][5:13] == 'xxx': 
		print (paperTitle)
=======
	try:
		tree = ET.parse(file[0])
		root = tree.getroot()
		paperTitle = root[1][0].find('title')
		if paperTitle==None:
			pass
			# print "Title not found:",file[0]
		else:
			paperTitle = paperTitle.text.lower().lstrip().rstrip().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip()
			stemmed = [ps.stem(word) for word in paperTitle.split()]
			paperTitle = " ".join(stemmed)
			paperTitle = paperTitle.replace(" ", "")
		

			# print paperTitle
			title_to_id[paperTitle] = file[0][5:13]
>>>>>>> fe9acd6518025ad1138b0ecfab6d95b6f8094c2c

		if paperTitle==None:
			titleAbsent.add(file[0][5:13])
		if file[0][5:13] == debug_title: print (paperTitle)
	except:
		pass

fp = open('db/MeaningfulCitationsDataset/ValenzuelaAnnotations.csv', 'r')

dataset = set()
dataset2 = set()
citingPapers = set()

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
	citingPapers.add(data[2])
	dataset.add((data[1], data[2]))
	sectionCount[(data[1], data[2])]={}
	for xx in sectionList:
		sectionCount[(data[1], data[2])][xx]=0

dataset2 = dataset.copy()
# print (('P05-1045', 'J12-4004') in dataset)
# print (('P05-1045', 'J12-4004') in dataset2)

def addSection(paperID, citationID, section):
	section = section.lower().lstrip().rstrip()
	if section=="": return
	# print (section)
	if (citationID, paperID) in dataset:
		for sec in sectionList:
			if sec in section:
				sectionCount[(citationID, paperID)][sec]+=1
				break
		else:
			sectionCount[(citationID, paperID)]["other"]+=1




for file in files:
	# if steps > MaxSteps: break	#comment this
<<<<<<< HEAD
	steps+=1
	if steps%10==0: print (steps)

	tree = ET.parse(file[0])
	root = tree.getroot()
	paperTitle = root[1][0].find('title')
	if paperTitle == None: paperTitle = ""
	else:
		paperTitle = paperTitle.text.lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")
		# if paperTitle[:2] == 'b\'': paperTitle = paperTitle[2:]


	# print file[0]
	tree = ET.parse(file[0])
	root = tree.getroot()
	citationList = next(root.iter('citationList'))
	totCit += len(citationList)
	if title_to_id[paperTitle] == debug_title:
		print ("starting")
		print(file)


	for citation in citationList:


		
		title = citation.find('title')
		booktitle = citation.find('booktitle')
		journal = citation.find('journal')
		if title != None: Onetitle = title.text
		elif booktitle!=None: Onetitle = booktitle.text
		elif journal!=None: Onetitle = journal.text
		else: Onetitle = ""	
		Onetitle = Onetitle.lstrip().rstrip().lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")

		paperID = None
		citationID = None
		for xx in title_to_id:
			if (paperTitle in xx) :
				paperID = title_to_id[xx]
				if paperID == debug_title:
					print("found")
					print(xx)
					print(file)

		for xx in title_to_id:
			if ((Onetitle in xx) or (xx in Onetitle)) and (Onetitle != '') and (xx != ''):
				citationID = title_to_id[xx]
=======
	try:
		tree = ET.parse(file[0])
		root = tree.getroot()
		paperTitle = root[1][0].find('title')
		if paperTitle == None: paperTitle = ""
		else:
			paperTitle = paperTitle.text.lower().lstrip().rstrip().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip()
			stemmed = [ps.stem(word) for word in paperTitle.split()]
			paperTitle = " ".join(stemmed)
			paperTitle = paperTitle.replace(" ", "")
	

			# if paperTitle[:2] == 'b\'': paperTitle = paperTitle[2:]

>>>>>>> fe9acd6518025ad1138b0ecfab6d95b6f8094c2c

		# print file[0]
		tree = ET.parse(file[0])
		root = tree.getroot()
		citationList = next(root.iter('citationList'))
		totCit += len(citationList)
		if title_to_id[paperTitle] == debug_title:
			print ("starting")

<<<<<<< HEAD
		if paperID == debug_title:
			print ((Onetitle, citationID))


		if citationID and paperID:
			pass
			# print title_to_id[paperTitle], paperTitle, '#', title_to_id[Onetitle], Onetitle
			
		# if paperID not in citingPapers: #no need to look at this pair
		# 	continue 

		if (citationID, paperID) in dataset:
			y+=1
			dataset2.remove((citationID, paperID))
			# print title_to_id[paperTitle], paperTitle, '#', title_to_id[Onetitle], Onetitle




		contexts = citation.find('contexts')
		if contexts==None: 
			# totalCitations[citationID] += 1
			# feature1[(citationID, paperID)] += 1
			pass
			# print "Reference without context:", Onetitle
		else:
			totalCitations[paperID] += len(contexts.findall('context'))
			if (citationID, paperID) not in dataset: continue
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
					elif child.tag == 'bodyText':
						# if child.get('confidence')=='0.953295307692308': print re.sub(r'[- \n\s]*','',alltext), "\nOVER\n", re.sub(r'[- \n\s]*','',context.text)
						if re.sub(r'[- \n\s\t]*','',alltext).lower().find(re.sub(r'[- \n\s\t]*','',context.text).lower())!=-1:
							# print ((Onetitle, curSection))
							curSection = curSection.rstrip().lstrip()
							# result = ''.join(i for i in curSection if not i.isdigit())
							result = curSection
							addSection(paperID, citationID, curSection)
							ans = result
							allSections.add(result)
							break

				#if ans == "": print "Not found", Onetitle

outf = open("output.csv", 'w')
outf.write("citaion, cited by, # direct citations, experiment, introduction, related work, discussion, conclusion, results, future work, other, f8\n")
for xx in dataset:
	outf.write(str(xx[0])+ ','+str(xx[1])+ ',')
	outf.write(str(feature1[xx])+ ',')
	for sec in sectionList: outf.write(str(sectionCount[xx][sec])+ ',')
	if totalCitations[xx[1]]!=0:
		outf.write(str(feature1[xx]*1.0/totalCitations[xx[1]]))
	else: outf.write('0')
	outf.write('\n')
=======
		i=0
		for citation in citationList:


			
			title = citation.find('title')
			booktitle = citation.find('booktitle')
			journal = citation.find('journal')
			if title != None: Onetitle = title.text
			elif booktitle!=None: Onetitle = booktitle.text
			elif journal!=None: Onetitle = journal.text
			else: Onetitle = ""
			Onetitle = Onetitle.lstrip().rstrip().lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip()
			stemmed = [ps.stem(word) for word in Onetitle.split()]
			Onetitle = " ".join(stemmed)
			Onetitle = Onetitle.replace(" ", "")
		

			paperID = None
			citationID = None
			for xx in title_to_id:
				if ((paperTitle in xx) or (xx in paperTitle)) and (xx != '') and (paperTitle != ''):
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
>>>>>>> fe9acd6518025ad1138b0ecfab6d95b6f8094c2c


# totalCitations = dict(totalCitations)
# topCited = sorted(totalCitations.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
# print topCited, len(totalCitations), totCit

# for xx in dataset.copy():
# 	if xx[0] in titleAbsent or xx[1] in titleAbsent:
# 		dataset.remove(xx)
<<<<<<< HEAD
print (dataset2)
=======
# print (dataset)
>>>>>>> fe9acd6518025ad1138b0ecfab6d95b6f8094c2c
print ((x,y))

# f1 = open("allSections.txt", "wb")
# for x in allSections: 
# 	f1.write(x+"\n")
<<<<<<< HEAD
# b using predicate argument structures for information extraction
# using predicate arguments structures for information extraction
=======
>>>>>>> fe9acd6518025ad1138b0ecfab6d95b6f8094c2c
