import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET

directories =[join("data/",d) for d in listdir("data/")]
files = []
paperauthors = []
matching = []
sameauthor_bool = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

for f in files:
    #print(f[0])
    foundauthor = 'False'
    paperauthors = []
    tree = ET.parse(f[0])
    root = tree.getroot()
    author_entries = root.findall('algorithm')
    #print (len(author_entries))
    for author in author_entries[1].iter('author'):
    	paperauthors.append(author.text)
    	#print(author.text);
    #print (paperauthors)
    for citation in root.iter('citationList'):
        for author in citation.iter('author'):
        	#if author.text in paperauthors:
        	#	matching.append(author.text)
       		#matching.append([author.text if author.text in paperauthors])
       		#print (author.text);
       		if (author.text in paperauthors):
       			foundauthor = 'True'
       	#print (matching)
       	sameauthor_bool.append(foundauthor);
    #print (foundauthor)
print (len(sameauthor_bool))
print (sameauthor_bool.count('False'))

outputfile = open('features_k4.txt','w')
i=0
for d in directories:
	#print (str(d[5:]) + " " + str(sameauthor_bool[i]) + "\n")
	outputfile.write(str(d[5:]) + " " + str(sameauthor_bool[i]) + "\n")
	i+=1
#print (i)
sys.exit()
