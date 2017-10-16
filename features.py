import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".xml"])

for f in files:
    print(f[0])
    tree = ET.parse(f[0])
    root = tree.getroot()
    for citation in root.iter('citationList'):
        <get_elements>
    sys.exit()
