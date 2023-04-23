# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import random
import ml_hw1_util as util


"""1. plot 10 samples, spaced uniformly in range [0,1], with the function sin(2pix) with a Gaussian noise."""
X_train, Y_train = util.plot_sin(10)


""" 2. Generate regression lines with polynomial basis function with order 1, 3, 5, 9, and 15."""
m1 = util.LinearRegression(1,0.1)
m1.fit(X_train, Y_train, 20)

m3 = util.LinearRegression(3,1)
m3.fit(X_train, Y_train, 10000)

m5 = util.LinearRegression(5,1)
m5.fit(X_train, Y_train, 10000)

m9 = util.LinearRegression(9,0.1)
m9.fit(X_train, Y_train, 10000)

m15 = util.LinearRegression(15,0.1)
m15.fit(X_train, Y_train, 10000)

order = ['1','3','5','9','15']
plt.figure(figsize=(12,6))
for i, model in enumerate([m1,m3,m5,m9,m15]):
    plt.subplot(2,3,i+1)
    model.plot_line(X_train, Y_train)
    plt.title('order'+order[i])
    plt.tight_layout()
plt.show()


""" 3. Add 2 or 3 points of exceptional outliers that do not follow sin(2πx) and then generate regression lines with
polynomial basis function with order 1, 3, 5, 9, and 15.
"""
X_outlier = X_train.copy().tolist()
Y_outlier = Y_train.copy().tolist()

for i in range(0,3):
    rand_idx = random.randint(0, len(X_train))
    X_outlier.insert(rand_idx, float(rand_idx)/float(len(X_train)))
    Y_outlier.insert(rand_idx, random.randint(5,15)/10.0)

X_outlier = np.array(X_outlier)
Y_outlier = np.array(Y_outlier)

plt.scatter(X_outlier, Y_outlier)
plt.show()

m1 = util.LinearRegression(1,0.1)
m1.fit(X_outlier, Y_outlier, 20)

m3 = util.LinearRegression(3,1)
m3.fit(X_outlier, Y_outlier, 10000)

m5 = util.LinearRegression(5,1)
m5.fit(X_outlier, Y_outlier, 10000)

m9 = util.LinearRegression(9,0.1)
m9.fit(X_outlier, Y_outlier, 10000)

m15 = util.LinearRegression(15,0.1)
m15.fit(X_outlier, Y_outlier, 10000)

order = ['1','3','5','9','15']
plt.figure(figsize=(12,6))
for i, model in enumerate([m1,m3,m5,m9,m15]):
    plt.subplot(2,3,i+1)
    model.plot_line(X_outlier, Y_outlier)
    plt.title('order'+order[i])
    plt.tight_layout()
plt.show()


""" 4. For the case including the outliers, generate the regression lines with the L2 regularization term with order 9
and 15. Show how the lines are changed with respect to λ . Generate the regression lines with the L1
regularization term and compare the lines with L2 regularization. 
"""
# lambda = 0.1
m9 = util.LR_regularization(9,0.1, lmda = 0.1)
m9.fit(X_outlier, Y_outlier, 10000)

m15 = util.LR_regularization(15,0.1, lmda = 0.1)
m15.fit(X_outlier, Y_outlier, 10000)

order = ['9','15']
plt.figure(figsize = (8,3))
for i, model in enumerate([m9,m15]):
    plt.subplot(1,2,i+1)
    model.plot_line(X_outlier, Y_outlier)
    plt.title('l2_reg_order'+order[i]+'_lambda=0.1')
    plt.tight_layout()
plt.show()

# lambda = 0.01
m9 = util.LR_regularization(9,0.1,lmda = 0.01)
m9.fit(X_outlier, Y_outlier, 10000)

m15 = util.LR_regularization(15,0.1, lmda = 0.01)
m15.fit(X_outlier, Y_outlier, 10000)

order = ['9','15']
plt.figure(figsize = (8,3))
for i, model in enumerate([m9,m15]):
    plt.subplot(1,2,i+1)
    model.plot_line(X_outlier, Y_outlier)
    plt.title('l2_reg_order'+order[i]+'_lambda=0.01')
    plt.tight_layout()
plt.show()

# lambda = 0.0001
m9 = util.LR_regularization(9,0.1,lmda = 0.0001)
m9.fit(X_outlier, Y_outlier, 10000)

m15 = util.LR_regularization(15,0.1,lmda = 0.0001)
m15.fit(X_outlier, Y_outlier, 10000)

order = ['9','15']
plt.figure(figsize = (8,3))
for i, model in enumerate([m9,m15]):
    plt.subplot(1,2,i+1)
    model.plot_line(X_outlier, Y_outlier)
    plt.title('l2_reg_order'+order[i]+'_lambda=0.0001')
    plt.tight_layout()
plt.show()

# L1 regularization
m9 = util.LR_regularization(9,0.1,reg = 'l1',lmda = 0.1)
m9.fit(X_outlier, Y_outlier, 10000)

m15 = util.LR_regularization(15,0.1,reg = 'l1', lmda = 0.1)
m15.fit(X_outlier, Y_outlier, 10000)

order = ['9','15']
plt.figure(figsize = (8,3))
for i, model in enumerate([m9,m15]):
    plt.subplot(1,2,i+1)
    model.plot_line(X_outlier, Y_outlier)
    plt.title('l1_reg_order'+order[i]+'_lambda=0.1')
    plt.tight_layout()
plt.show()


"""
 5. Plot 100 samples with the function sin(2πx) instead of 10 samples, and then generate the regression lines with
order 1, 3, 5, 9, and 15.
"""
X_train_big, Y_train_big = util.plot_sin(100)

m1 = util.LinearRegression(1,0.1)
m1.fit(X_train_big, Y_train_big, 20)

m3 = util.LinearRegression(3,1)
m3.fit(X_train_big, Y_train_big, 10000)

m5 = util.LinearRegression(5,1)
m5.fit(X_train_big, Y_train_big, 10000)

m9 = util.LinearRegression(9,0.1)
m9.fit(X_train_big, Y_train_big, 10000)

m15 = util.LinearRegression(15,0.1)
m15.fit(X_train_big, Y_train_big, 10000)

order = ['1','3','5','9','15']
plt.figure(figsize = (12,6))
for i, model in enumerate([m1,m3,m5,m9,m15]):
    plt.subplot(2,3,i+1)
    model.plot_line(X_train_big, Y_train_big)
    plt.title('order'+order[i])
    plt.tight_layout()
plt.show()