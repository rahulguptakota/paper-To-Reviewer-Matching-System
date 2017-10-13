from requests import get
from urllib.parse import urljoin
from os import path, getcwd
from bs4 import BeautifulSoup as soup
from sys import argv
import sys
import csv
import os

#Inorder to downloads all the pdfs please change the corressponding paths


def get_page(base_url):
	req= get(base_url)
	if req.status_code==200:
		return req.text

def get_all_links(html):
	bs= soup(html,'html.parser')
	links= bs.findAll('a')
	return links

def get_pdf(base_url,papers, base_dir):
	html= get_page(base_url)
	links= get_all_links(html)
	n_pdfs= 0
	for link in links:
		try:	
			if link.get('href') in papers:
				os.mkdir(base_dir + "/" + link.get('href')[:-4]);
				papers.remove(link.get('href'))
				n_pdfs+= 1
				content= get(urljoin(base_url, link.get('href')))
				with open(path.join(base_dir+ "/" + link.get('href')[:-4], link.text+'.pdf'), 'wb') as pdf:
					pdf.write(content.content)
		except:
			print("Operation failed.")

if __name__=='__main__':
	urls = []
	papers = []
	with open('/home/charlie/Documents/paper-To-Reviewer-Matching-System/MeaningfulCitationsDataset/MeaningfulCitationsDataset/ValenzuelaAnnotations.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			url = "http://aclweb.org/anthology/" + row[1][0] + "/"+row[1][0:3]+"/"
			if url not in urls:
				urls.append(url)
			url = "http://aclweb.org/anthology/" + row[2][0] + "/"+row[2][0:3]+"/"
			if url not in urls:
				urls.append(url) 
			if(row[2] not in papers):
				papers.append(row[2]+".pdf")
			if(row[1] not in papers):
				papers.append(row[1]+".pdf")
	for url in urls:
		get_pdf(base_url=url, papers=papers, base_dir="/home/charlie/Documents/data")