# -*- coding: utf-8 -*-
"""
Created on Mon May 09 2016

@author: jmlee
"""
import sys
import classificationMethod
import numpy as np
import util
import scipy.optimize

MIN_SUPPORT_VECTOR_MULTIPLIER = 1e-5

class SupportVectorMachine(classificationMethod.ClassificationMethod):
    def __init__(self, legalLabels, type, data):
        self.legalLabels = legalLabels
        self.type = type

        self.kernel = lambda x, y: np.exp(-np.linalg.norm(x - y) ** 2 / (2 * self.sigma ** 2))

        self.supportMultipliers = {}
        self.supportVectors = {}
        self.supportVectorLabels = {}
        self.biases = {}
        self.data = data

        if self.data == 'faces':
            self.sigma = 4 # kernel parameter
            self.C = 10 # slack variable penalty parameter
        else:
            self.sigma = 3 # kernel parameter
            self.C = 1 # slack variable penalty parameter


    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method
        """

        """
        Perform multi-class classification via One-vs-one reduction.
        Train C(C-1)/2 binary clasifiers for C-way multiclass problem
        """
        for c1 in range(len(self.legalLabels)):
            for c2 in range(c1+1, len(self.legalLabels)):
                # c1: +1 / c2: -1
                X1 = np.asarray([x for i,x in enumerate(trainingData) if trainingLabels[i] == c1]) # Data with label c1
                X2 = np.asarray([x for i,x in enumerate(trainingData) if trainingLabels[i] == c2]) # Data with label c1
                X = np.vstack((X1, X2))
                t = np.concatenate((np.ones(X1.shape[0]), -np.ones(X2.shape[0])))

                lagrangeMultipliers = self.trainSVM(X, t, self.C, self.kernel)
                supportVectorIndices = lagrangeMultipliers > MIN_SUPPORT_VECTOR_MULTIPLIER
                self.supportMultipliers[(c1,c2)] = lagrangeMultipliers[supportVectorIndices]
                self.supportVectors[(c1,c2)] = X[supportVectorIndices]
                self.supportVectorLabels[(c1,c2)] = t[supportVectorIndices]
                self.biases[(c1,c2)] = np.mean(
                    [y - self.predictSVM(
                        x, self.supportMultipliers[(c1,c2)], self.supportVectors[(c1,c2)], self.supportVectorLabels[(c1,c2)], 0, self.kernel
                    )
                    for (x, y) in zip(self.supportVectors[(c1,c2)], self.supportVectorLabels[(c1,c2)])]
                )

    def quadraticProgrammingSolver(self, P, q, G, h, A, b):
        """
        This method solves the quadratic programming with the following form:

        minimize (1/2) x^T P x + q^T x
        s.t. Gx <= h
              Ax = b

        OUTPUT : solution 'x'.

        * Do not modify this method *
        """

        func = lambda x, sign=1.0, P=P, q=q: 0.5 * np.dot(np.dot(x, P), x) + np.dot(q, x)
        func_deriv = lambda x, sign=1.0, P=P, q=q: 0.5 * np.dot(P + P.T, x) + q
        constraints = []
        for i in range(A.shape[0]):
            constraints.append({
                'type': 'eq',
                'fun': lambda x, A=A, b=b, i=i: b[i] - np.dot(A[i, :], x),
                'jac': lambda x, A=A, i=i: -A[i, :]
            })
        for i in range(G.shape[0]):
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, G=G, h=h, i=i: h[i] - np.dot(G[i, :], x),
                'jac': lambda x, A=A, i=i: -G[i, :]
            })
        cons = tuple(constraints)
        x0 = np.zeros(P.shape[0])
        solution = scipy.optimize.minimize(func, x0, jac=func_deriv, constraints=cons, method='SLSQP')
        return solution.x

    def trainSVM(self, X, t, C, kernel):
        """
        X : (N x D)-sized numpy array
        t : N-sized numpy array. t[i] = -1 or +1
        C : Slack variable penalty parameter
        kernel : RBF kernel function. Use this like: kernel(x, y)

        - N : the number of training instances
        - D : the number of features (PCA was used for feature extraction)

        OUTPUT : Lagrange multipliers 'a_1,...,a_N'. N-sized Numpy array
        """

        N, D = X.shape
        t_ = t.reshape((-1, 1))
        K = np.array([[kernel(x_n, x_m) for x_m in X] for x_n in X])
        P = np.dot(t_, t_.T) * K
        q = np.empty(N)
        q.fill(-1)
        G = np.identity(N)
        h = np.empty(N)
        h.fill(C)
        A = np.zeros((N, N))
        A[0] = t
        b = np.zeros((N, 1))

        return self.quadraticProgrammingSolver(P, q, G, h, A, b).flatten()

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.counts = [] # Counts are stored for later data analysis (autograder).
        for datum in testData:
            count = np.zeros(len(self.legalLabels))
            for c1 in range(len(self.legalLabels)):
                for c2 in range(c1 + 1, len(self.legalLabels)):
                    predict = self.predictSVM(datum,
                                              self.supportMultipliers[(c1,c2)],
                                              self.supportVectors[(c1,c2)],
                                              self.supportVectorLabels[(c1,c2)],
                                              self.biases[(c1,c2)],
                                              self.kernel)
                    if predict > 0:
                        count[c1] += 1
                    else:
                        count[c2] += 1

            guesses.append(np.argmax(count))
            self.counts.append(count)

        return guesses

    def predictSVM(self, x, supportMultipliers, supportVectors, supportVectorLabels, bias, kernel):
        """
        Fill in this function!
        x : test datum. D-sized numpy array.
        supportMulutipliers : Lagrange multipliers whose values are larger than some threshold (1e-5). M-sized numpy array.
        supportVectors : Support vectors. (M x D)-sized numpy array.
        supportVectorLabels : Labels of support vectors(+1 or -1). M-sized numpy array.
        bias : bias term for prediction.
        kernel : RBF kernel function. Use this like: kernel(x, y).

        - M : the number of support vectors (usually, M is much smaller than the total number of training data N)

        OUTPUT : Prediction result. The output should be +1 or -1 (scalar).
        """

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

        return 1

