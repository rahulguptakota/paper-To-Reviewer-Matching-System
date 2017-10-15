import unicodedata
import sys
from os import listdir
from os.path import isfile, join

directories =[join("data/",d) for d in listdir("data/")]
files = []

for d in directories:
    files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-4:]==".txt"])

for f in files:
    print(f)
    try:
        fd= open(f[0],'r+')
        data = fd.read()
        normal = str(unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')).replace('\\n', '\n')
        fd1 = open(f[0][:-4]+"_1.txt","w")
        fd1.write(normal)
        fd1.close()
        fd.close()
    except:
        print("Operation failed.")
