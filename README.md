# paper-To-Reviewer-Matching-System
Paper to Reviewer Assignment is a tedious but a very crucial job for conference organizers. Till date the Toronto Paper Matching System (TPMS) is a widely used tool to solve this problem but the results of this system are not found to be up to the mark. We aim to build a better system by taking into account the structure and semantic analysis of the paper to be reviewed.

#Files and Usage
1) scrape.py: This file is used to download all the pdf files of papers that we are going to use as our data.
2) pdftotext.bash: This bash file is used to create the txt file of all the pdf files of research papers.
3) remove_diacritics.py: This file is used to remove diacritics from original txt files the output is stored in "_1.txt" of respective file.


features_k6.py->
	returns features_k6.txt where the corresponding feature is of the following type -
		-> paper_id(id) number_of_citations_that_appear_in_tablecaption(n). Then 2*n lines follow where (2*i -1) line gives paper id and (2*i) line has title of the citation.
		e.g.
			S13-1002 1 
			H05-1079
			recognising textual entailment with logical inference

feature_k7.py->
	return features_k7.txt where each line has paper_id (1/number_of_references)

feature_k9.py->
	returns features_k9.txt where each line has (cited_paper_id) (citing_paper_id) (tfidf score)

features_k4.py - 
This file is used to extract feature of a paper. This feature is 1 for a paper if the authors has cited their other paper in the citations otherwise 0.

features_k4.txt - This file contains the extracted features from features_k4.py. This file has two columns. On every row, first column contains paper ACL id and second column contains feature value corresponding to this paper.

features_k10.py - This file is used to calculate Page Rank Score of every paper.

features_k10.txt - This file contains the extracted features from features_k10.py. This file has two columns. On every row, first column contains paper ACL id and second column contains Page Rank score corresponding to this paper.

features_k12.py - This file is used to extract feature of a paper. It does topic modelling using NMF over 20 topics. For every paper, one gets a 20 length vector containing scores corresponding to every topic.

features_k12.txt - This file contains the extracted features from features_k12.py. This file has two columns. On every row, first column contains paper ACL id and second column contains vector of length 20(containing scores for every topic).				 