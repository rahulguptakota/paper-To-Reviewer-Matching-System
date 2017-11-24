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
import csv
ps = PorterStemmer()

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

# print (files)
# sys.exit()

totalCitations = defaultdict(int)
steps = 0
MaxSteps = 50
totCit = 0
title_to_id = defaultdict(str)
allSections = set()
debug_title = 'xxx'
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
			paperTitle = paperTitle.text.lower().translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lstrip().rstrip().replace(" ", "")
			# print paperTitle
			title_to_id[paperTitle] = file[0][5:13]

		if paperTitle==None:
			titleAbsent.add(file[0][5:13])
		#if file[0][5:13] == debug_title or file[0][5:13] == 'xxx': 
			#print (paperTitle)
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



#files = ["data/W09-1116/parsedData.xml"]
for file in files:
	# if steps > MaxSteps: break	#comment this
	steps+=1
	#if steps%10==0: print (steps)
	try:
		#print("hello")
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
		#if title_to_id[paperTitle] == debug_title:
			#print ("starting")
			#print(file)
		citationStrings=[]
		citeSentences=[]
		#print (file[0])

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
				#print("Reference without context:", Onetitle)
				pass
			else:            
				for context in contexts.findall('context'):
					citationStrings.append(context.attrib['citStr'])				

		for citation in citationList.iter('citation'):	
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
					#if paperID == debug_title:
						#print("found")
						#print(xx)
						#print(file)

			for xx in title_to_id:
				if ((Onetitle in xx) or (xx in Onetitle)) and (Onetitle != '') and (xx != ''):
					citationID = title_to_id[xx]


			#if paperID == debug_title:
				#print ((Onetitle, citationID))


			#if citationID and paperID:
			#	pass
				# print title_to_id[paperTitle], paperTitle, '#', title_to_id[Onetitle], Onetitle
				
			# if paperID not in citingPapers: #no need to look at this pair
			#  	continue 
			if (citationID, paperID) in dataset:
				y+=1
				dataset2.remove((citationID, paperID))	
				# print title_to_id[paperTitle], paperTitle, '#', title_to_id[Onetitle], Onetitle



			#print("hello")
			contexts = citation.find('contexts')			
			#sys.exit()
			#mn print ("1")
			if contexts==None: 
				# totalCitations[citation/ID] += 1
				# feature1[(citationID, paperID)] += 1
				pass
				# print "Reference without context:", Onetitle
			else:
				totalCitations[paperID] += len(contexts.findall('context'))
				if (citationID, paperID) not in dataset: continue
				feature1[(citationID, paperID)] += len(contexts.findall('context'))
				# print (Onetitle, len(contexts.findall('context')), totalCitations[Onetitle])
				#print (citationID)
				#print (paperID)
				#print(citationStrings)
				for context in contexts.findall('context'):
					text = context.text
					for citationStr in citationStrings:
						#print(citationStr)
						text = re.sub(r'\([ ,]*'+re.escape(citationStr)+'[ ,]*\)','CITATION', text)
						text = text.replace(citationStr, 'CITATION')
					sentences = text.split(". ")
					# sentences = sent_tokenize(text)
					# print(sentences)
					# time.sleep(1)
					citeSentences += filter(lambda sent: "CITATION" in sent, sentences)
		# sys.exit()
		# print (citeSentences)
				#sys.exit()
		#print (str(file[0].split("/")[1]))
		print (str(file[0].split("/")[0]) + "/" + paperID + "/citeSents2.csv")
		print (paperID)
		print (citationID)
		#out_file = open('temp.txt','w')
		with open(str(file[0].split("/")[0]) + "/" + paperID + "/citeSents2.csv","w") as f:
			#f.write("2\n")
			#print("bingo1")
			# print(f)
			# print ("1")
			#print (citeSentences)
			wr = csv.writer(f, delimiter="\n")
			#print (citeSentences)
			citeSentences = list(set(citeSentences))

			for ele in citeSentences:
				#print([ele+",,"])
				#f.write(str([ele+",,"+"\n"]))
				wr.writerow([ele+",,"])
			#print("bingo2")	

		#print("bingo3")
				# f.write([ele+",,"])
		#print(citeSentences);
		# break
		#exit()
	except:
		#print("hello")
		pass
				#if ans == "": print "Not found", Onetitle
sys.exit()
outf = open("output1.csv", 'w')
outf.write("citaion, cited by, # direct citations, experiment, introduction, related work, discussion, conclusion, results, future work, other, f8\n")
for xx in dataset:
	if xx in dataset2: continue
	outf.write(str(xx[0])+ ','+str(xx[1])+ ',')
	outf.write(str(feature1[xx])+ ',')
	for sec in sectionList: outf.write(str(sectionCount[xx][sec])+ ',')
	if totalCitations[xx[1]]!=0:
		outf.write(str(feature1[xx]*1.0/totalCitations[xx[1]]))
	else: outf.write('0')
	outf.write('\n')


# totalCitations = dict(totalCitations)
# topCited = sorted(totalCitations.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
# print topCited, len(totalCitations), totCit

# for xx in dataset.copy():
# 	if xx[0] in titleAbsent or xx[1] in titleAbsent:
# 		dataset.remove(xx)
# print (dataset2)
print ((x,y))

# f1 = open("allSections.txt", "wb")
# for x in allSections: 
# 	f1.write(x+"\n")
# b using predicate argument structures for information extraction
# using predicate arguments structures for information extraction
