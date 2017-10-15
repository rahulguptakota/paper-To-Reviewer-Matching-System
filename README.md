# paper-To-Reviewer-Matching-System
Paper to Reviewer Assignment is a tedious but a very crucial job for conference organizers. Till date the Toronto Paper Matching System (TPMS) is a widely used tool to solve this problem but the results of this system are not found to be up to the mark. We aim to build a better system by taking into account the structure and semantic analysis of the paper to be reviewed.

#Files and Usage
1) scrape.py: This file is used to download all the pdf files of papers that we are going to use as our data.
2) pdftotext.bash: This bash file is used to create the txt file of all the pdf files of research papers.
3) remove_diacritics.py: This file is used to remove diacritics from original txt files the output is stored in "_1.txt" of respective file.
