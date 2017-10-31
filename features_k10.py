import sys
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import islice
import numpy as np
from scipy.sparse import csc_matrix
#from PageRank import PageRanker
import networkx as nx

def pageRank(G, s = .85, maxerr = .001):
    """
    Computes the pagerank for each of the n states.
    Used in webpage ranking and text summarization using unweighted
    or weighted transitions respectively.
    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.
    Kwargs
    ----------
    s: probability of following a transition. 1-s probability of teleporting
       to another state. Defaults to 0.85
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged. Defaults to 0.001
    """
    n = G.shape[0]
    #print (n)

    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in range(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            Ti = np.ones(n) / float(n)

            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )

    # return normalized pagerank
    return r/sum(r)

'''
graph = {}
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if row[1] in graph.keys() and not row[0] in graph[row[1]]:
			graph[row[1]].append(row[0])
		else:
			graph[row[1]] = [row[0],]	

'''


edges = {}
i=0
j=0
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if i==0:
			i=1
		else:
			if not row[0] in edges:
				edges[row[0]] = j
				j+=1
			if not row[1] in edges:
				edges[row[1]] = j
				j+=1

#print (j)
#print (edges)

g = np.zeros((j,j))

i=0
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if i==0:
			i=1
		else:
			g[edges[row[1]]][edges[row[0]]] = 1

#print (g[0])
print (g.shape)
#G = g[0:10,0:10]
#print (G)
#pagerank_score = pageRank(g,s=0.86)
Gr = nx.DiGraph(g)
pr = nx.pagerank(Gr, alpha=0.9)
result = np.array(pr);
print (pr[0])
sys.exit()

# for a,b in graph.items():
# 	print(a,b)	

#f9 starts from here
'''
i = 0
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if i==0:
			i=1

		else:	
			paper1 = join("data/",row[0]) + "/parsedData.xml"
			paper2 = join("data/",row[1]) + "/parsedData.xml"
			print(paper1,paper2)
			tree1 = ET.parse(paper1)
			root1 = tree1.getroot()
			tree2 = ET.parse(paper2)
			root2 = tree2.getroot()
			vect = TfidfVectorizer(min_df=1)
			variant1 = root1[1][0]
			variant2 = root2[1][0]
			abstract1 = variant1.find('abstract')
			abstract2 = variant2.find('abstract')
			if abstract1 and abstract2:
				tfidf = vect.fit_transform([abstract2.text,abstract1.text])
				print((tfidf * tfidf.T).A)
			i+=1
			print(i)

'''
