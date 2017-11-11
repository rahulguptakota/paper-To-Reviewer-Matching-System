import xml.etree.ElementTree as ET
import re
import time
import os, csv
from nltk.tokenize import sent_tokenize
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 
stop_words = set(stopwords.words('english'))

train = []
test = []
rootDir = './data'
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
	fo = open("/home/grahul/paper-To-Reviewer-Matching-System/data/A00-1019" + "/citeSents.csv", "r")
	lines = fo.readlines()
	for line in lines:
		print(line)
		line = line.strip()
		splitsent = line.split(",,")
		word_tokens = word_tokenize(splitsent[0])
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		line = " ".join(filtered_sentence)
		train.append((filtered_sentence, splitsent[1]))
		test.append((filtered_sentence, splitsent[1]))
	break

cl = NaiveBayesClassifier(train)
print(cl.classify("It is also possible to focus on non-compositional compounds, a key point in bilingual applications (CITATION; CITATION; Lin, 99)"))  # "pos"
print(cl.classify("I don't like their pizza."))  # "neg"
print(cl.accuracy(test))

print(cl.show_informative_features())
