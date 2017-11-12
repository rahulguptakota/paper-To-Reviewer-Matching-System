import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET
import csv

directories =[join("data/",d) for d in listdir("data/")]
files = []
paperauthors = []
matching = []
sameauthor_bool = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

graph = {}
outputfile = open('features_k4.txt','w')
with open('index.csv', newline='') as csvfile:
  i = 0
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
  for row in spamreader:
    if i ==0: 
      i+=1
      continue
    n1 = join("data/", row[1])
    n2 = join("data/",row[0])
    x1 = ""
    x2 = ""
    for f in listdir(n1):
      if isfile(join(n1, f)) and f[-4:]==".xml":
        x1 = join(n1,f)
    for f in listdir(n2):
      if isfile(join(n2, f)) and f[-4:]==".xml":
        x2 = join(n2,f)    
    # print(x1,x2)
    paperauthors1 = []
    tree1 = ET.parse(x1)
    root1 = tree1.getroot()
    author_entries1 = root1.findall('algorithm')
    #print (len(author_entries))
    for author in author_entries1[1].iter('author'):
      paperauthors1.append(author.text)
      #print(author.text);
    # print (paperauthors1)
    paperauthors2 = []
    tree2 = ET.parse(x2)
    root2 = tree2.getroot()
    author_entries2 = root2.findall('algorithm')
    #print (len(author_entries))
    for author in author_entries2[1].iter('author'):
      paperauthors2.append(author.text)
      #print(author.text);
    # print (paperauthors2)
    if len(set(paperauthors2).intersection(paperauthors1)) > 0:
      outputfile.write(row[0] + " "+  row[1]  + " 1" +"\n")
      i+=1
    else :
      outputfile.write(row[0] + " "+ row[1] + " 0" +"\n")

print(i)
# i = 0
# for f1 in files:
#   name1 = f1[0].split("/")[1]
#   for f2 in files:
#     name2 = f2[0].split("/")[1]
#     if name1 in graph.keys():
#       if name2 in graph[name1]:
#         paperauthors1 = []
#         tree1 = ET.parse(f1[0])
#         root1 = tree1.getroot()
#         author_entries1 = root1.findall('algorithm')
#         #print (len(author_entries))
#         for author in author_entries1[1].iter('author'):
#           paperauthors1.append(author.text)
#           #print(author.text);
#         # print (paperauthors1)
#         paperauthors2 = []
#         tree2 = ET.parse(f2[0])
#         root2 = tree2.getroot()
#         author_entries2 = root2.findall('algorithm')
#         #print (len(author_entries))
#         for author in author_entries2[1].iter('author'):
#           paperauthors2.append(author.text)
#           #print(author.text);
#         # print (paperauthors2)
#         if len(set(paperauthors2).intersection(paperauthors1)) > 0:
#           outputfile.write(name1 + " "+  name2  + " 1" +"\n")
#         else :
#           outputfile.write(name1 + " "+ name2 + " 0" +"\n")  
#   i+=1
# #   print(i) 



# for f in files:
#     #print(f[0])
#     foundauthor = 'False'
#     paperauthors = []
#     tree = ET.parse(f[0])
#     root = tree.getroot()
#     author_entries = root.findall('algorithm')
#     #print (len(author_entries))
#     for author in author_entries[1].iter('author'):
#     	paperauthors.append(author.text)
#     	#print(author.text);
#     #print (paperauthors)
#     for citation in root.iter('citationList'):
#         for author in citation.iter('author'):
#         	#if author.text in paperauthors:
#         	#	matching.append(author.text)
#        		#matching.append([author.text if author.text in paperauthors])
#        		#print (author.text);
#        		if (author.text in paperauthors):
#        			foundauthor = 'True'
#        	#print (matching)
#        	sameauthor_bool.append(foundauthor);
#     #print (foundauthor)
# print (len(sameauthor_bool))
# print (sameauthor_bool.count('False'))

# outputfile = open('features_k4.txt','w')
# i=0
# for d in directories:
# 	#print (str(d[5:]) + " " + str(sameauthor_bool[i]) + "\n")
# 	outputfile.write(str(d[5:]) + " " + str(sameauthor_bool[i]) + "\n")
# 	i+=1
# #print (i)
# sys.exit()
