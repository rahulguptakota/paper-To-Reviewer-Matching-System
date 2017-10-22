import sys
from os import listdir
from os.path import isfile, join
# from nltk.tokenize import sent_tokenize
# import nltk
import xml.etree.ElementTree as ET
import requests
import json
from bs4 import BeautifulSoup

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

for f in files:
    print(f[0])
    fd1 = open(f[0][:-4]+"_reference_papers.txt","w")
    tree = ET.parse(f[0])
    root = tree.getroot()
    for citation in root.iter('citation'):
        try:
            print(citation.find('title').text)
            s = requests.get('http://www.google.com/search?q='+citation.find('title').text)
            soup =BeautifulSoup(s.content,'html.parser')
            print(soup.find_all('h3', {"class"='r'))
            # print(urlencode(citation.find('title').text))
            # soup = BeautifulSoup(requests.get("https://www.google.com/?gws_rd=ssl#q=" +citation.find('title').text), "html.parser")
            # print("https://www.google.com/?gws_rd=ssl#q=" +citation.find('title').text)
            # for item in soup.find_all('div'):
            #     print(item.string)
            # sys.exit()
            fd1.write(citation.find('title').text + "\n")
        except:
            print("No title in the xml file")
    fd1.close()
    sys.exit()
