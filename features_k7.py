import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET

directories =[join("data/",d) for d in listdir("data/")]
files = []
inverseref_count = []
out_file = open('features_k7.txt','w')

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

for f in files:
	print(f[0])
	count_references=0
	tree = ET.parse(f[0])
	root = tree.getroot()
	for citation in root.iter('citation'):
	  count_references = count_references + 1
	print (1/count_references);
	inverseref_count.append(1/count_references)
	out_file.write(f[0].split("/")[1] + " " + str((1.0/count_references)) + "\n")

sys.exit()
