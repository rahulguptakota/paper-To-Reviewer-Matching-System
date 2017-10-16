import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
from spacy.en import English
en = English()

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-6:]=="_1.txt"])

for f in files:
    fd= open(f[0],'r+')
    data = fd.read()
    doc = en(data)
    for s in list(doc.sents):
        print(s.string)
    sys.exit()
    paragraphs = [p for p in text.split('\n') if p]
    print(paragraphs[-1])
    #print(data)
    ttt = nltk.tokenize.TextTilingTokenizer()
    sent_tokenize_list = sent_tokenize(data)
    para = ttt.tokenize(data)
    #print(sent_tokenize_list)
    print(para[-1])
    #print(para[-1])
    sys.exit()
    fd1 = open(f[0][:-4]+"_1.txt","w")
    fd1.write(normal)
    fd1.close()
    fd.close()
