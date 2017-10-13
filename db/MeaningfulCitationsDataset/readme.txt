Meaningful Citations Dataset
============================

This is the readme file for the "Meaningful Citations" dataset.


The data consists of 630 citations, one in each row.

The fields are:

- Annotator
  An identifier for the annotator that labeled the citation. This does not reveal
  the identity of the annotator, but it lets us know which citations were annotated
  by the same person

- Paper
  The cited paper. This field uses the paper's ACL ID.
  For example, paper A00-1043 is "Sentence Reduction for Automatic Text Summarization"
  as can be seen here: http://www.aclweb.org/anthology/A00-1043

- Cited-by
  The citing paper. This field also uses the paper's ACL ID.

- Follow-up
  A label assigned to the citation by the annotatator. This label is an ordinal
  value that goes from 0 to 3 that represent how meaningful the citation is to
  the citing paper's work, according to the annotator.




Identifying Meaningful Citations
Marco Valenzuela, Vu Ha and Oren Etzioni
In AAAI 2015, Workshop on Scholarly Big Data
