from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import KFold
from random import shuffle
from sklearn.svm import SVC
from sklearn import preprocessing
import numpy as np

files = ["k4","k7","k9","k10"]
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
        try:
            data[(line[0],line[1])][f] = line[-1]
        except:
            pass
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
        # print(line)
        data_dhawal[(line[0],line[1])] = {}
        data_dhawal[(line[0],line[1])][f] = line[2:]
        # print(data[(line[0],line[1])])
        data_dhawal[(line[0],line[1])]["test"] = data[(line[0],line[1])]["test"]
        for f1 in files:
            data_dhawal[(line[0],line[1])][f1] = data[(line[0],line[1])][f1]
        # print(line)
        i = i + 1
    fd.close()


# rahulfile = ["semantic.csv"]
# for f in rahulfile:
#     fd = open(f,'rb')
#     t = fd.read()
#     i=0
#     for line in t.decode().split("\n"):
#         line = line.split(",")
#         print(line)
#         data_dhawal[(line[0],line[1])][f] = line[-1]
#         # print(line)
#         i = i + 1
#     fd.close()
# print(data_dhawal)
# exit()
X = []
Y = []
for key in data_dhawal.keys():
    # print(key)
    # try:
    temp = []
    for f in files:
        temp.append(data_dhawal[key][f])
    for t in data_dhawal[key]["output.csv"]:
        temp.append(t)
    # for t in data_dhawal[key]["semantic.csv"]:
    #     temp.append(t)
    # temp.append(t for t in data_dhawal[key]["output.csv"])
    X.append(temp)
    Y.append(data_dhawal[key]['test'])
    # except:
    #     pass
# print(X[1])
# exit()
# print(Y)
Y = np.array(Y)
kf = KFold(n_splits=5)
X = preprocessing.scale(X)

globalaccuracy = 0
globalaccuracy1 = 0
globalsvmaccuracy = 0
globaldecisiontreeaccuracy = 0
globalknnaccuracy = 0

for train_index, test_index in kf.split(X):
    # print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    # print(Y)
    y_train, y_test = Y[train_index], Y[test_index]
    # print("The size of X_train, X_test, y_train, y_test is {}, {}, {}, {}".format(np.shape(X_train),np.shape(X_test),np.shape(y_train),np.shape(y_test)))
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
    clf2 = KNeighborsClassifier(n_neighbors=4)
    clf3 = SVC(kernel='rbf', probability=True)

    eclf = VotingClassifier(estimators=[('dt', clf1), ('knn', clf2), ('svc', clf3)])
    # clf1 = clf1.fit(X_train,y_train)
    # clf2 = clf2.fit(X_train,y_train)
    # clf3 = clf3.fit(X_train,y_train)
    eclf = eclf.fit(X_train,y_train)
    eclf_accuracy = eclf.score(X_test,y_test)
    prediction = eclf.predict(X_test)
    cm = confusion_matrix(y_test, prediction)
    globalaccuracy += eclf_accuracy
    # print("The accracy for Voting classifier is ",eclf_accuracy)
    # print("The cm for Voting classifier is \n",cm)

    svmclf = SVC(kernel='rbf', probability=True)
    svmclf = svmclf.fit(X_train,y_train)
    svmclf_accuracy = svmclf.score(X_test,y_test)
    prediction = svmclf.predict(X_test)
    cm = confusion_matrix(y_test, prediction)
    globalsvmaccuracy += svmclf_accuracy
    # print("The accracy for SVM classifier is ",svmclf_accuracy)
    # print("The cm for Voting classifier is \n",cm)

    dtclf = DecisionTreeClassifier(max_depth=7)
    dtclf = dtclf.fit(X_train,y_train)
    dtclf_accuracy = dtclf.score(X_test,y_test)
    prediction = dtclf.predict(X_test)
    cm = confusion_matrix(y_test, prediction)
    globaldecisiontreeaccuracy += dtclf_accuracy
    print("The importance of Features in DT is {}".format(dtclf.feature_importances_))
    # print("The accracy for SVM classifier is ",dtclf_accuracy)
    # print("The cm for Voting classifier is \n",cm)

    knnclf = KNeighborsClassifier(n_neighbors=5)
    knnclf = knnclf.fit(X_train,y_train)
    knnclf_accuracy = knnclf.score(X_test,y_test)
    prediction = knnclf.predict(X_test)
    cm = confusion_matrix(y_test, prediction)
    globalknnaccuracy += knnclf_accuracy
    # print("The accracy for SVM classifier is ",knnclf_accuracy)
    # print("The cm for Voting classifier is \n",cm)


    eclf = VotingClassifier(estimators=[('dt', clf1), ('svc', clf3)], voting='soft', weights=[2,2])
    bclf = BaggingClassifier(base_estimator=eclf)
    bclf = bclf.fit(X_train,y_train)
    bclf_accuracy = bclf.score(X_test,y_test)
    prediction = bclf.predict(X_test)
    cm = confusion_matrix(y_test, prediction)
    globalaccuracy1 += bclf_accuracy
    # print("The accracy for bagging Voting classifier is ",bclf_accuracy)
    # print("The cm for bagging Voting classifier is \n",cm)

print("The accracy for Voting classifier is ",globalaccuracy/5)
print("The accracy for bagging Voting classifier is ",globalaccuracy1/5)
print("The accracy for SVM classifier is ",globalsvmaccuracy/5)
print("The accracy for Decision Tree classifier is ",globaldecisiontreeaccuracy/5)
print("The accracy for KNN classifier is ",globalknnaccuracy/5)
# adaclf = AdaBoostClassifier(base_estimator=SVC(kernel='linear', probability=True),n_estimators=100)
# # accracy = cross_val_score(adaclf, X_test, y_test)
# # accuracy = cross_val_score(adaclf, X, Y)
# adaclf = adaclf.fit(X_train,y_train)
# adaclf_accuracy = adaclf.score(X_test,y_test)
# prediction = adaclf.predict(X_test)
# cm = confusion_matrix(y_test, prediction)
# print("Accuracy is ",adaclf_accuracy)
# print("The confusion matrix is:\n",cm)