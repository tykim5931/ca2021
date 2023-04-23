# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random

PI=3.14159265359

def plot_sin(point_num):
    X = np.linspace(0, 1, 100)
    Y = np.sin(X*2*np.pi)
    plt.plot(X, Y, color = 'limegreen')

    x = np.linspace(0, 1, point_num)
    y = np.array(np.sin([2*PI*i for i in x])).reshape(1,point_num)
    noise = np.random.normal(0, 0.2, size=point_num)
    y_noise = (y+noise).reshape((point_num,))
    plt.scatter(x, y_noise, color = 'dodgerblue')
    
    plt.show()
    return x, y_noise

class LinearRegression():
    def __init__(self, degree, lr):
        self.degree = degree
        self.param = np.random.normal(scale=0.01,size=degree+1) 
        self.lr = lr

    def fit(self, X, Y, epochs):
        for epoch in range(epochs):

            # calculate gradient, cost
            gradient = np.zeros(shape = self.param.shape)
            cost = 0
            for x, y in zip(X, Y): 
                h = 0
                for i, p in enumerate(self.param): 
                    h += p*(x**i)  
                for i in range(self.degree+1):  
                    gradient[i] += (h-y)*(x**i)
                cost += (h-y)**2  

            gradient *= self.lr/float(len(X))   
            cost /= 2*len(X)   

            # update parameters
            for i in range(self.degree+1):
                self.param[i] -= gradient[i]   
            # if(epoch == 0 or epoch == epochs/2 or epoch+1 == epochs):
            #     print("epoch:%d cost: %f"%(epoch,cost))
        print("Linear Regression with degree " + str(self.degree) + f": cost {cost}")
        return self.param

    def plot_line(self, X, Y):
        # plot the polynomial line
        x_axis = np.linspace(0, 1, 100)
        fx = []
        for i, x in enumerate(x_axis):
            x_lst = np.array([x**j for j in range(self.degree+1)])
            fx.append(np.sum(x_lst*self.param))
        plt.plot(x_axis, fx, color = 'limegreen')
        plt.scatter(X, Y)


class LR_regularization(LinearRegression):
    def __init__(self, degree, lr, reg = 'l2', lmda = 1):
        self.degree = degree
        self.param = np.random.normal(scale=0.01,size=degree+1) 
        self.lr = lr
        self.reg = reg
        self.lmda = lmda

    def fit(self, X, Y, epochs):
        for epoch in range(epochs):

            # calculate gradient, cost
            gradient = np.zeros(shape = self.param.shape)
            cost = 0
            for x, y in zip(X, Y): 
                h = 0
                for i, p in enumerate(self.param):  
                    h += p*(x**i)  
                for i in range(self.degree+1):  
                    gradient[i] += (h-y)*(x**i)
                cost += (h-y)**2   

            gradient *= self.lr/float(len(X))   
            cost /= 2*len(X)    

            # update parameters
            if self.reg == 'l2':
                for i in range(self.degree+1):
                    self.param[i] -= (gradient[i] + self.lmda*self.param[i]/float(len(X)))
            elif self.reg == 'l1':
                for i in range(self.degree+1):
                    reg_grad = 0   
                    if(self.param[i] == 0):
                        reg_grad = 0
                    else:
                        reg_grad = self.param[i] / abs(self.param[i])
                    self.param[i] -= (gradient[i] + self.lmda*reg_grad)
            # if(epoch == 0 or epoch == epochs/2 or epoch+1 == epochs):
            #     print("epoch:%d cost: %f"%(epoch,cost))

        print("Linear Regression with degree " + str(self.degree) + f": cost {cost}")
        return self.param