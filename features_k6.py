import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET

directories =[join("data/",d) for d in listdir("data/")]
files = []
inverseref_count = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

huny = 0
for f in files:
	huny += 1
	# print(f[0])
	count_references=0
	tree = ET.parse(f[0])
	root = tree.getroot()
	result = {}
	#print(root)
	#print(root[2][0][0][5][0].attrib['citStr'])
	citationlist = root[2][0]
	# variant = root.findall('tablecaption')
	# print(len(variant))
	# print(len(citationlist))
	y = len(citationlist)
	x = 0
	i=0
	z=0
	k = 0
	# print("citation list size: ", y)
	for citation in citationlist:
	  contexts = citation.find('contexts')
	  search = ""
	  if contexts:
	  	#print("hello")
	  	for context in contexts:
	  		x+=1
	  		search = context.attrib['citStr']
	  		if(search in result.keys()):
	  			k+=1
	  		else:	
	  			result[search] = 0
	  		flag = 0
	  		for tablecaption in root.iter('tableCaption'):
	  			i = i+1
	  			if search and search in tablecaption.text:
	  				# print(f[0], search)
	  				result[search] = 1
	  			#print(tablecaption.text, search)
	  else:
	  	search = citation.find('marker').text
	  	if(search in result.keys()):
	  			k+=1
	  	else:
	  		result[search] = 0
	  	flag = 0
	  	z = z+ 1
	  	for tablecaption in root.iter('tableCaption'):
	  		i = i+ 1
	  		if search and search in tablecaption.text:
	  			# print(f[0], search)
	  			result[search] = 1
	  		#print(tablecaption.text, search)
	  	#print(citation.find('marker').text)		
	  	#print("nye")
	# print(i, x, z, k) 
	#print(result, len(result)) 	
	if huny ==20 :
		exit()
    # print (1/count_references);
    # inverseref_count.append(1/count_references)

sys.exit()
