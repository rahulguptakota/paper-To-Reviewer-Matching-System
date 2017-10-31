import xml.etree.ElementTree as ET
import re
import sys
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import operator 

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

# print files

totalCitations = defaultdict(int)
steps = 0
MaxSteps = 500
totCit = 0

for file in files:
	if steps > MaxSteps: break

	print file[0]
	tree = ET.parse(file[0])
	root = tree.getroot()
	citationList = next(root.iter('citationList'))
	totCit += len(citationList)
	for citation in root.iter('citation'):
		title = citation.find('title')
		booktitle = citation.find('booktitle')
		journal = citation.find('journal')
		if title != None: Onetitle = title.text
		elif booktitle!=None: Onetitle = booktitle.text
		elif journal!=None: Onetitle = journal.text
		else: Onetitle = "Title not found"
		Onetitle = Onetitle.lstrip().rstrip()

		contexts = citation.find('contexts')
		if contexts==None: 
			totalCitations[Onetitle] += 1
			print "Reference without context:", Onetitle
		else:
			totalCitations[Onetitle] += len(contexts.findall('context'))
			# print Onetitle, len(contexts.findall('context')), totalCitations[Onetitle]
			for context in contexts.findall('context'):
				steps += 1
				SectLabel = root[0][0]	#0 is SectLabel, variant 0
				curSection = ""
				ans = ""
				alltext = ""
				for child in SectLabel:
					if child.text!=None: alltext+=child.text
					if child.tag == 'sectionHeader': curSection = child.text
					elif child.tag == 'bodyText':
						# if child.get('confidence')=='0.953295307692308': print re.sub(r'[- \n\s]*','',alltext), "\nOVER\n", re.sub(r'[- \n\s]*','',context.text)
						if re.sub(r'[- \n\s\t]*','',alltext).find(re.sub(r'[- \n\s\t]*','',context.text))!=-1:
							# print Onetitle, curSection
							ans = curSection
							break

				if ans == "": print "Not found", Onetitle


totalCitations = dict(totalCitations)
topCited = sorted(totalCitations.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
print topCited, len(totalCitations), totCit