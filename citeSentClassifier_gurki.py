import xml.etree.ElementTree as ET
import re
import time
import os, csv
from nltk.tokenize import sent_tokenize
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn import naive_bayes
from random import shuffle 
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from prettyprint import pp
import os, re, pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score, recall_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, NuSVC, SVC
from sklearn.grid_search import GridSearchCV
from datetime import datetime as dt
from ipy_table import *

def testClassifier(x_train, y_train, x_test, y_test, clf, name):
    """
    this method will first train the classifier on the training data
    and will then test the trained classifier on test data.
    Finally it will report some metrics on the classifier performance.
    
    Parameters
    ----------
    x_train: np.ndarray
             train data matrix
    y_train: list
             train data label
    x_test: np.ndarray
            test data matrix
    y_test: list
            test data label
    clf: sklearn classifier object implementing fit() and predict() methods
    
    Returns
    -------
    metrics: list
             [training time, testing time, recall and precision for every class, macro-averaged F1 score]
    """
    metrics = []
    start = dt.now()
    clf.fit(x_train, y_train)
    end = dt.now()
    print 'training time: ', (end - start)
    pickle.dump( clf, open( name+".p", "wb" ) )
    # add training time to metrics
    metrics.append(end-start)
    
    start = dt.now()
    yhat = clf.predict(x_test)
    end = dt.now()
    print 'testing time: ', (end - start)
    
    # add testing time to metrics
    metrics.append(end-start)
    
    print 'classification report: '
#     print classification_report(y_test, yhat)
    pp(classification_report(y_test, yhat))
    
    print 'f1 score'
    print f1_score(y_test, yhat, average='macro')
    
    print 'accuracy score'
    print accuracy_score(y_test, yhat)
    
    precision = precision_score(y_test, yhat, average=None)
    recall = recall_score(y_test, yhat, average=None)
    
    # add precision and recall values to metrics
    for p, r in zip(precision, recall):
        metrics.append(p)
        metrics.append(r)
    
    
    #add macro-averaged F1 score to metrics
    metrics.append(f1_score(y_test, yhat, average='macro'))
    
    print 'confusion matrix:'
    print confusion_matrix(y_test, yhat)
    
    # plotting the confusion matrix
    plt.imshow(confusion_matrix(y_test, yhat), interpolation='nearest')
    # plt.show()
    
    return metrics


stop_words = set(stopwords.words('english'))
clfrNB = naive_bayes.MultinomialNB()
train = []
test = []
rootDir = './data_label'
one_label = 0
zero_label = 0
ps = PorterStemmer()
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
    try:
        # print(dirName)
        fo = open(dirName + "/citeSents.csv", "r")
    except:
        continue
    lines = fo.readlines()
    for line in lines:
        line = line.strip().lower()
        # print(line)
        splitsent = line.split(",,")
        # print(splitsent)
        word_tokens = word_tokenize(splitsent[0])
        if splitsent[1] != '1' and splitsent[1] != '0' :
            print(splitsent)
        elif splitsent[1] == "1":
            one_label += 1
        else:
            zero_label += 1
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        line = " ".join(filtered_sentence)
        stemmed = [ps.stem(word) for word in line.split()]
        stemmed = filter(lambda x: not(len(x)<3 or re.findall(r"[0-9]+",x)) , stemmed)
        stemmed = list(stemmed)
        line = " ".join(stemmed)
        # print(line)
        train.append((line, splitsent[1]))

shuffle(train)
# testindex = int(len(train)*4/5)
# test = train[testindex:]
# train = train[:testindex]

train_arr = []
# test_arr = []
train_lbl = []
# test_lbl = []
for x in train:
    train_arr.append(x[0])
    train_lbl.append(x[1])
# for x in test:
# 	test_arr.append(x[0])
    # test_lbl.append(x[1])

vectorizer = CountVectorizer()
vectorizer.fit(train_arr)
train_mat = vectorizer.transform(train_arr)
print train_mat
# print train_mat.shape
# test_mat = vectorizer.transform(test_arr)
# print test_mat.shape

tfidf = TfidfTransformer()
tfidf.fit(train_mat)
train_tfmat = tfidf.transform(train_mat)
print train_tfmat.shape
print train_tfmat[0]
# test_tfmat = tfidf.transform(test_mat)
# print test_tfmat.shape
testindex = int(len(train)*4/5)
test_tfmat = train_tfmat[testindex:]
test_lbl = train_lbl[testindex:]
train_tfmat = train_tfmat[:testindex]
train_lbl = train_lbl[:testindex]

metrics_dict = []

bnb = BernoulliNB()
bnb_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, bnb, "bernoulliNB")
metrics_dict.append({'name':'BernoulliNB', 'metrics':bnb_me})

gnb = GaussianNB()
gnb_me = testClassifier(train_tfmat.toarray(), train_lbl, test_tfmat.toarray(), test_lbl, gnb, "guassianNB")
metrics_dict.append({'name':'GaussianNB', 'metrics':gnb_me})

mnb = MultinomialNB()
mnb_me = testClassifier(train_tfmat.toarray(), train_lbl, test_tfmat.toarray(), test_lbl, mnb, "MultinomialNB")
metrics_dict.append({'name':'MultinomialNB', 'metrics':mnb_me})

for nn in [5]:
    print 'knn with ', nn, ' neighbors'
    knn = KNeighborsClassifier(n_neighbors=nn)
    knn_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, knn, "knn"+str(nn))
    metrics_dict.append({'name':'5NN', 'metrics':knn_me})
    print ' '

print("linear SVM starts:")
lsvm = LinearSVC( class_weight={'1': 1, '0' : 1})
lsvm_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, lsvm, "linearSVM")
metrics_dict.append({'name':'LinearSVM', 'metrics':lsvm_me})

rbfsvm = SVC(kernel = 'poly',degree=2,coef0=1 ,class_weight={'1': zero_label, '0' : one_label})
rbfsvm_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, rbfsvm, "rbfSVM")
metrics_dict.append({'name':'SVM with RBF kernel', 'metrics':rbfsvm_me})

bnb_params = {'alpha': [a*0.1 for a in range(0,11)]}
bnb_clf = GridSearchCV(BernoulliNB(), bnb_params, cv=10)
bnb_clf.fit(train_tfmat, train_lbl)
print 'best parameters'
print bnb_clf.best_params_
best_bnb = BernoulliNB(alpha=bnb_clf.best_params_['alpha'])
best_bnb_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, best_bnb,"bernoulliNB")
metrics_dict.append({'name':'Best BernoulliNB', 'metrics':best_bnb_me})

best_gnb = GaussianNB()
best_gnb_me = testClassifier(train_tfmat.toarray(), train_lbl, test_tfmat.toarray(), test_lbl, best_gnb, "guassianNB")
metrics_dict.append({'name':'Best GaussianNB', 'metrics':best_gnb_me})

mbn_params = {'alpha': [a*0.1 for a in range(0,11)]}
mbn_clf = GridSearchCV(MultinomialNB(), mbn_params, cv=10)
mbn_clf.fit(train_tfmat, train_lbl)
print 'best parameters'
print mbn_clf.best_params_
best_mbn = MultinomialNB(alpha=mbn_clf.best_params_['alpha'])
best_mbn_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, best_mbn, "MultinomialNB")
metrics_dict.append({'name':'Best MultinomialNB', 'metrics':best_mbn_me})

print metrics_dict

# knn_params = {'n_neighbors': range(1,21), 'weights': ['uniform', 'distance'], 'algorithm': ['ball_tree', 'kd_tree'],
#               'leaf_size': [15, 30, 50, 100], 'p': [1,2]}
# knn_clf = GridSearchCV(KNeighborsClassifier(), knn_params, cv=10)
# knn_clf.fit(train_tfmat, train_lbl)
# print 'best parameters'
# print knn_clf.best_params_
# best_knn = KNeighborsClassifier(n_neighbors=knn_clf.best_params_['n_neighbors'], weights=knn_clf.best_params_['weights'],
#                                 algorithm=knn_clf.best_params_['algorithm'], leaf_size=knn_clf.best_params_['leaf_size'])
# best_knn_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, best_knn)
# metrics_dict.append({'name':'Best KNN', 'metrics':best_knn_me})

# nusvm = NuSVC()
# nusvm_me = testClassifier(train_tfmat, train_lbl, test_tfmat, test_lbl, nusvm)
# metrics_dict.append({'name':'nuSVM', 'metrics':nusvm_me})    
# traindata = [data[0] for data in train]
# trainlabel = [data[1] for data in train]
# clfrNB.fit(traindata, trainlabel)
# print(test)
# cl = NaiveBayesClassifier(train)
# print(cl.classify("It is also possible to focus on non-compositional compounds, a key point in bilingual applications (CITATION; CITATION; Lin, 99)"))  # "pos"
# print(cl.classify("I don't like their pizza."))  # "neg"
# for item in test:
# 	if(cl.classify(item[0]) == '1'):
# 		print(item, cl.classify(item[0]))
# print(cl.accuracy(test))

# print(cl.show_informative_features(100))
# print(train)
