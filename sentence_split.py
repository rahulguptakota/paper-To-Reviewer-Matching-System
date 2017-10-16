import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-6:]=="_1.txt"])

for f in files:
    fd= open(f[0],'r+')
    data = fd.read()
    print(data)
    sent_tokenize_list = sent_tokenize(data)
    print(sent_tokenize_list)
    sys.exit()
    fd1 = open(f[0][:-4]+"_1.txt","w")
    fd1.write(normal)
    fd1.close()
    fd.close()
