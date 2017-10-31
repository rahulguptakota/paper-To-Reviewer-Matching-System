import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import islice

graph = {}
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if row[1] in graph.keys() and not row[0] in graph[row[1]]:
			graph[row[1]].append(row[0])
		else:
			graph[row[1]] = [row[0],]	
		
# for a,b in graph.items():
# 	print(a,b)	

#f9 starts from here
i = 0
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if i==0:
			i=1

		else:	
			paper1 = join("data/",row[0]) + "/parsedData.xml"
			paper2 = join("data/",row[1]) + "/parsedData.xml"
			print(paper1,paper2)
			tree1 = ET.parse(paper1)
			root1 = tree1.getroot()
			tree2 = ET.parse(paper2)
			root2 = tree2.getroot()
			vect = TfidfVectorizer(min_df=1)
			variant1 = root1[1][0]
			variant2 = root2[1][0]
			abstract1 = variant1.find('abstract')
			abstract2 = variant2.find('abstract')
			if abstract1 and abstract2:
				tfidf = vect.fit_transform([abstract2.text,abstract1.text])
				print((tfidf * tfidf.T).A)
			i+=1
			print(i)
