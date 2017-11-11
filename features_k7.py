import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET
import csv


directories =[join("data/",d) for d in listdir("data/")]
files = []
inverseref_count = []
out_file = open('features_k7.txt','w')

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

result = {}

for f in files:
	# print(f[0])
	count_references=0
	tree = ET.parse(f[0])
	root = tree.getroot()
	for citation in root.iter('citation'):
	  count_references = count_references + 1
	inverseref_count.append(1/count_references)
	# out_file.write(f[0].split("/")[1] + " " + str((1.0/count_references)) + "\n")
	global result
	result[str(f[0].split("/")[1]) ] = (1.0/count_references)
	print(str(f[0].split("/")[1]), (1.0/count_references))

graph = {}
i=0
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if row[1] in graph.keys() and not row[0] in graph[row[1]]:

			graph[row[1]].append(row[0])
		else:
			graph[row[1]] = [row[0],]
		print(str(row[0]), str(row[1]))
		if i> 0:
			out_file.write(str(row[0]) + " " + str(row[1]) + " " + str(result[str(row[0])]) + "\n")	
		i+=1
sys.exit()
