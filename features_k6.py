import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET

directories =[join("data/",d) for d in listdir("data/")]
files = []
inverseref_count = []
out_file = open('features_k6.txt','w')

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

map_title_id = {}
map_id_title = {}

for f in files:
	tree = ET.parse(f[0])
	root = tree.getroot()
	title = "None"
	if root[1][0].find('title') is not None:
		title = root[1][0].find('title').text.lower()
		if title not in map_title_id:
			x = title.replace('\n', ' ')
			map_title_id[x] = f[0].split("/")[1];
			map_id_title[f[0].split("/")[1]] = x

	else:
		print f[0].split("/")[1]

huny = 0
for f in files:
	count_references=0
	tree = ET.parse(f[0])
	root = tree.getroot()
	result = {}
	result_title = {}	
	check = {}
	citationlist = root[2][0]
	y = len(citationlist)
	x = 0
	i=0
	z=0
	k = 0
	for citation in citationlist:
	  contexts = citation.find('contexts')
	  search = ""
	  if contexts:
	  	for context in contexts:
	  		paper_title = citation.find('title')
	  		if paper_title is not None:
	  			paper_title = paper_title.text
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
		  				result[search] = 1
		  				# print search
		  				# if paper_title is not None:
		  				# 	print search
		  				# 	if paper_title.text:
		  				# 		if paper_title.text not in result_title:
		  				# 			print paper_title.text

		  				if paper_title and paper_title not in result_title:
		  					# print paper_title
		  					result_title[paper_title] = 1 
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
	  			result[search] = 1

	  			
	out_file.write(f[0].split("/")[1] + " " + str(len(result_title)) + "\n")
	# print f[0].split("/")[1], len(result_title)
	for key, value in result_title.iteritems() :
		str_key = key.replace('\n', ' ')
		str_key = str_key.rstrip('.').lower()
		print str_key
		if str_key in map_title_id:
			out_file.write(map_title_id[str_key]+"\n"+ str_key + "\n")
		else:
			out_file.write("None"+"\n"+ str_key + "\n")

sys.exit()
