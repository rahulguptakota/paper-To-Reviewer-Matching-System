from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier

files = ["k4","k7","k9","k10","k12"]
# ,"features_k6.txt","features_k7.txt","features_k9.txt","features_k10.txt","features_k12.txt"]
dhawalfile = ["output.csv"] 


data = {}

fd = open("db/MeaningfulCitationsDataset/ValenzuelaAnnotations1.csv",'rb')
t = fd.read()
i=0
for line in t.decode().split("\n"):
    if i != 0:
        line = line.split(",")
        try:
            data[(line[1],line[2])] = {}
            data[(line[1],line[2])]["test"] = line[-1]
            # print(line)
        except:
            pass
    i = i + 1
fd.close()

# print(data)

for f in files:
    fd = open("features_" + f + ".txt",'rb')
    t = fd.read()
    i=0
    for line in t.decode().split("\n"):
        line = line.split(" ")
        data[(line[0],line[1])][f] = line[-1]
        # print(line)
        i = i + 1
    fd.close()
# print(data)
data_dhawal = {}
for f in dhawalfile:
    fd = open(f,'rb')
    t = fd.read()
    i=0
    for line in t.decode().split("\n"):
        line = line.split(",")
        data_dhawal[(line[0],line[1])] = {}
        data_dhawal[(line[0],line[1])][f] = line[2:]
        print(data[(line[0],line[1])])
        data_dhawal[(line[0],line[1])]["test"] = data[(line[0],line[1])]["test"]
        for f1 in files:
            data_dhawal[(line[0],line[1])][f1] = data[(line[0],line[1])][f1]
        # print(line)
        i = i + 1
    fd.close()
print(data_dhawal)
X = []
Y = []
for key in data_dhawal.keys():
    temp = []
    for f in files:
        temp.append(data_dhawal[key][f])
    for t in data_dhawal[key]["output.csv"]:
        temp.append(t)
    # temp.append(t for t in data_dhawal[key]["output.csv"])
    X.append(temp)
    Y.append(data_dhawal[key]['test'])
print(X[1])
print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state = 0)
print("The size of X_train, X_test, y_train, y_test is {}, {}, {}, {}".format(np.shape(X_train),np.shape(X_test),np.shape(y_train),np.shape(y_test)))
# svm_model_linear = SVC(kernel = 'rbf', gamma=5).fit(X_train, y_train)
# svm_predictions = svm_model_linear.predict(X_test)
# # model accuracy for X_test  
# accuracy = svm_model_linear.score(X_test, y_test)
# # creating a confusion matrix
# cm = confusion_matrix(y_test, svm_predictions)
# print("The accuracy for SVM is ", accuracy)
# print("The confusion matrix for SVM is\n",cm)
# # training a KNN classifier
# knn = KNeighborsClassifier(n_neighbors = 7).fit(X_train, y_train)

clf1 = DecisionTreeClassifier(max_depth=4)
clf2 = KNeighborsClassifier(n_neighbors=7)
clf3 = SVC(kernel='rbf', probability=True)

eclf = VotingClassifier(estimators=[('dt', clf1), ('knn', clf2), ('svc', clf3)], voting='soft', weights=[2,1,2])
# clf1 = clf1.fit(X_train,y_train)
# clf2 = clf2.fit(X_train,y_train)
# clf3 = clf3.fit(X_train,y_train)
eclf = eclf.fit(X_train,y_train)
eclf_accuracy = eclf.score(X_test,y_test)
prediction = eclf.predict(X_test)
cm = confusion_matrix(y_test, prediction)
print("The accracy for Voting classifier is ",eclf_accuracy)
print("The cm for Voting classifier is \n",cm)

eclf = VotingClassifier(estimators=[('dt', clf1), ('svc', clf3)], voting='soft', weights=[2,2])
bclf = BaggingClassifier(base_estimator=eclf)
bclf = bclf.fit(X_train,y_train)
bclf_accuracy = bclf.score(X_test,y_test)
prediction = bclf.predict(X_test)
cm = confusion_matrix(y_test, prediction)
print("The accracy for bagging Voting classifier is ",eclf_accuracy)
print("The cm for bagging Voting classifier is \n",cm)

# adaclf = AdaBoostClassifier(base_estimator=SVC(kernel='linear', probability=True),n_estimators=100)
# # accracy = cross_val_score(adaclf, X_test, y_test)
# # accuracy = cross_val_score(adaclf, X, Y)
# adaclf = adaclf.fit(X_train,y_train)
# adaclf_accuracy = adaclf.score(X_test,y_test)
# prediction = adaclf.predict(X_test)
# cm = confusion_matrix(y_test, prediction)
# print("Accuracy is ",adaclf_accuracy)
# print("The confusion matrix is:\n",cm)