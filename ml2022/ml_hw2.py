import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_openml

# Fetch MNIST DATA
mnist = fetch_openml('mnist_784')

# Look into MNIST DATA
print("MNIST data shape: ", mnist.data.shape)
print("Lable data shape: ", mnist.target.shape)
print("MNIST data labels: ", np.sort(list(mnist['target'].unique())))
print("MNIST example: ")
sample_img = np.array(mnist.data.iloc[0], dtype='uint8')
sample_img = sample_img.reshape((28,28))
plt.imshow(sample_img, cmap='gray')

mnist_small_data = mnist.data[:7000]
mnist_small_target = mnist.target[:7000]
print(mnist_small_target.value_counts())

from sklearn.model_selection import train_test_split

# split data into training set and test set
x_train, x_test, y_train, y_test = train_test_split(mnist_small_data, 
                                                    mnist_small_target, 
                                                    test_size = 1/7.0, 
                                                    random_state = 0)
train_size = 5000
x_train, x_val = x_train[:train_size], x_train[train_size:]
y_train, y_val = y_train[:train_size], y_train[train_size:]
print("Training size: ", x_train.shape)
print("Validation size: ", x_val.shape)
print("Test size: ", x_test.shape)



# Logistic Regression Model
from sklearn.linear_model import LogisticRegression

logisticReg1 = LogisticRegression() # Default L2 norm
logisticReg1.fit(x_train, y_train) # Train MNIST
score1 = logisticReg1.score(x_val, y_val)

logisticReg2 = LogisticRegression(penalty="none") # without Regularization
logisticReg2.fit(x_train, y_train)
score2 = logisticReg2.score(x_val, y_val)

logisticReg3 = LogisticRegression(solver = 'liblinear', penalty="l1") # L1 norm
logisticReg3.fit(x_train, y_train)
score3 = logisticReg3.score(x_val, y_val)

print("Regularization: L2, Accuracy: ", score1)
print("Regularization: None, Accuracy: ", score2)
print("Regularization: L1, Accuracy: ", score3)

for iters in [300,500,1000]:
    logisticReg = LogisticRegression(max_iter = iters) # Default L2 norm
    logisticReg.fit(x_train, y_train) # Train MNIST
    score1 = logisticReg.score(x_val, y_val)
    print(f"Max_iter: {iters},   Accuracy: {score1}")

# Best of Logistic Regression
logisticReg = LogisticRegression(max_iter = 500) # Default L2 norm
logisticReg.fit(x_train, y_train) # Train MNIST



# KNN Classifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification

for k in [2,3,4,5,7,9,11]:
    knn = KNeighborsClassifier(n_neighbors=k, n_jobs=1) # n_jobs: core for training
    knn.fit(x_train, y_train)
    score = knn.score(x_val, y_val)
    print(f"{k}-Neighbors Classifier, Accuracy:  {score}")

# Best of KNN
knnClassifier = KNeighborsClassifier(n_neighbors=5, n_jobs=1)
knnClassifier.fit(x_train, y_train)



# SVM classifiers
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

for c in [0.1, 1, 100]:
    l_svm = LinearSVC(random_state = 822)
    l_svm.fit(x_train, y_train)
    score = l_svm.score(x_val, y_val)
    print(f"Linear SVM, C: {c}, Accuracy: {score}")

for kernel in ['linear', 'rbf', 'poly']:
    svm = SVC(kernel=kernel)
    svm.fit(x_train, y_train)
    score = svm.score(x_val, y_val)
    print(f"SVM, Kernel: {kernel}, C: 1.0,    Accuracy: {score}")

for c_try in [10, 100, 1000, 10000]:
    svmGauss = SVC(kernel='rbf', C=c_try)
    svmGauss.fit(x_train, y_train)
    score = svmGauss.score(x_val, y_val)
    print(f"SVM, Kernel: rbf, C: {c_try},    Accuracy: {score}")

for gamma in [1e-09, 1e-08, 0.0000001, 0.00001, 0.001]:
    svmGauss = SVC(kernel='rbf', C=10, gamma = gamma, 
                    decision_function_shape='ovo')
    svmGauss.fit(x_train, y_train)
    score = svmGauss.score(x_val, y_val)
    print(f"SVM, Kernel: rbf, C: 10, gamma: {gamma},   Accuracy: {score}")

# Best of SVMs
svmClassifier = SVC(kernel='rbf', C=10, gamma="scale")  #scale = 1/(n_features*X.var())
svmClassifier.fit(x_train, y_train)



# Random forest classifiers
from sklearn.ensemble import RandomForestClassifier

for num_trees in [1, 10, 100, 1000]:
    rf = RandomForestClassifier(n_estimators=num_trees, random_state = 822)
    rf.fit(x_train, y_train)
    score = rf.score(x_val, y_val)
    print(f"n_estimators: {num_trees},  Accuracy: {score}")

import math 

rf_sqrt = RandomForestClassifier(random_state = 228, n_estimators = 100) 
                                            #default, sqrt(features)
rf_log = RandomForestClassifier(random_state = 228, n_estimators = 100, 
                                            max_features = round(math.log2(784)))
rf_naive = RandomForestClassifier(random_state = 228, n_estimators = 100, 
                                            max_features = 784)

rf_log.fit(x_train, y_train)
rf_sqrt.fit(x_train, y_train)
rf_naive.fit(x_train, y_train)

print(f"max_features: sqrt(featurs), Accuracy: {rf_sqrt.score(x_val, y_val)}")
print(f"max_features: log2(784), Accuracy: {rf_log.score(x_val, y_val)}")
print(f"max_features: 784, Accuracy: {rf_naive.score(x_val, y_val)}")

# Best of RF
rfClassifier = RandomForestClassifier(random_state = 7, n_estimators = 1000)#default, sqrt(features)
rfClassifier.fit(x_train, y_train)



# get accuracy on test set
print(f"Logistic Regression Classifier's Accuracy: {logisticReg.score(x_test, y_test)}")
print(f"KNN Classifier's Accuracy:                 {knnClassifier.score(x_test, y_test)}")
print(f"SVM Classifier's Accuracy:                 {svmClassifier.score(x_test, y_test)}")
print(f"Random Forest Classifier's Accuracy:       {rfClassifier.score(x_test, y_test)}")