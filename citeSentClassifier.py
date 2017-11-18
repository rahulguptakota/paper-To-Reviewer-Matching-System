import xml.etree.ElementTree as ET
import re
import time
import os, csv
from nltk.tokenize import sent_tokenize
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
 
stop_words = set(stopwords.words('english'))

train = []
test = []
rootDir = './data_label'
ps = PorterStemmer()
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
	try:
		print(dirName)
		fo = open(dirName + "/citeSents.csv", "r")
	except:
		continue
	lines = fo.readlines()
	for line in lines:
		line = line.strip().lower()
		# print(line)
		splitsent = line.split(",,")
		# print(splitsent)
		word_tokens = word_tokenize(splitsent[0])
		if splitsent[1] != '1' and splitsent[1] != '0' :
			print(splitsent)
		# elif splitsent[1] == "1":
		# 	print(splitsent)
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		line = " ".join(filtered_sentence)
		stemmed = [ps.stem(word) for word in line.split()]
		stemmed = filter(lambda x: not(len(x)<3 or re.findall(r"[0-9]+",x)) , stemmed)
		stemmed = list(stemmed)
		line = " ".join(stemmed)
		# print(line)
		train.append((line, splitsent[1]))

testindex = int(len(train)*4/5)
test = train[testindex:]
train = train[:testindex]
# print(test)
cl = NaiveBayesClassifier(train)
# print(cl.classify("It is also possible to focus on non-compositional compounds, a key point in bilingual applications (CITATION; CITATION; Lin, 99)"))  # "pos"
# print(cl.classify("I don't like their pizza."))  # "neg"
for item in test:
	if(cl.classify(item[0]) == '1'):
		print(item, cl.classify(item[0]))
print(cl.accuracy(test))

print(cl.show_informative_features(100))
# print(train)
