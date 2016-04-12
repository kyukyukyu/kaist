# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 2016

@author: jphong
"""
import classificationMethod
import numpy as np
import util

class LogisticRegressionClassifier(classificationMethod.ClassificationMethod):
  def __init__(self, legalLabels, type, seed):
    self.legalLabels = legalLabels
    self.type = type
    self.learningRate = [0.01, 0.001, 0.0001]
    self.l2Regularize = [1.0, 0.1, 0.0]
    self.numpRng = np.random.RandomState(seed)
    self.initialWeightBound = None
    self.posteriors = []
    self.costs = []
    self.epoch = 1000

    self.bestNCorrect = 0
    self.bestParam = None # You must fill in this variable in validateWeight

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method.
    Iterates several learning rates and regularization parameter to select the best parameters.

    Do not modify this method.
    """
    for lRate in self.learningRate:
      curCosts = []
      for l2Reg in self.l2Regularize:
        self.initializeWeight(trainingData.shape[1], len(self.legalLabels))
        for i in xrange(self.epoch):
          cost, grad = self.calculateCostAndGradient(trainingData, trainingLabels)
          self.updateWeight(grad, lRate, l2Reg)
          curCosts.append(cost)
        self.validateWeight(validationData, validationLabels)
        self.costs.append(curCosts)

  def initializeWeight(self, featureCount, labelCount):
    """
    Initialize weights and bias with randomness.

    Do not modify this method.
    """
    if self.initialWeightBound is None:
      initBound = 1.0
    else:
      initBound = self.initialWeightBound
    self.W = self.numpRng.uniform(-initBound, initBound, (featureCount, labelCount))
    self.b = self.numpRng.uniform(-initBound, initBound, (labelCount, ))

  @staticmethod
  def softmax(c, Wx, b):
    Y = Wx + b
    m = np.max(Y)
    Y_shifted = Y - np.full_like(Y, m)
    return (np.exp(Y_shifted[c]) / np.sum(np.exp(Y_shifted)))

  def calculateCostAndGradient(self, trainingData, trainingLabels):
    """
    Fill in this function!

    trainingData : (N x D)-sized numpy array
    trainingLabels : N-sized list
    - N : the number of training instances
    - D : the number of features (PCA was used for feature extraction)
    RETURN : (cost, grad) python tuple
    - cost: python float, negative log likelihood of training data
    - grad: gradient which will be used to update weights and bias (in updateWeight)

    Evaluate the negative log likelihood and its gradient based on training data.
    Gradient evaluted here will be used on updateWeight method.
    Note the type of weight matrix and bias vector:
    self.W : (D x C)-sized numpy array
    self.b : C-sized numpy array
    - D : the number of features (PCA was used for feature extraction)
    - C : the number of legal labels
    """
    N, _ = trainingData.shape
    C = len(self.legalLabels)
    cost = 0
    grad = (np.zeros(self.W.shape), np.zeros(self.b.shape))
    XW = np.dot(trainingData, self.W)
    m = np.amax(XW, axis=1)
    XW_shifted = XW - np.repeat(m, C).reshape((-1, C))
    XW_shifted_exp = np.exp(XW_shifted)
    i = 0
    while i < N:
      x_i = trainingData[i]
      y_i = trainingLabels[i]
      Wx_shifted = XW_shifted[i]
      Wx_shifted_exp = XW_shifted_exp[i]
      cost += Wx_shifted[y_i] - np.log(np.sum(Wx_shifted_exp))
      for c in self.legalLabels:
        mu = self.softmax(c, XW[i], self.b)
        coeff = mu - (1 if c == y_i else 0)
        grad[0][:, c] += coeff * x_i
        grad[1][c] += coeff
      i += 1

    return cost, grad

  def updateWeight(self, grad, learningRate, l2Reg):
    """
    Fill in this function!
    grad : gradient which was evaluated in calculateCostAndGradient
    learningRate : python float, learning rate for gradient descent
    l2Reg: python float, L2 regularization parameter

    Update the logistic regression parameters using gradient descent.
    Update must include L2 regularization.
    Please note that bias parameter must not be regularized.
    """
    self.W -= learningRate * (grad[0] + l2Reg * self.W)
    self.b -= learningRate * grad[1]

  def validateWeight(self, validationData, validationLabels):
    """
    Fill in this function!

    validationData : (M x D)-sized numpy array
    validationLabels : M-sized list
    - M : the number of validation instances
    - D : the number of features (PCA was used for feature extraction)

    Choose the best parameters of logistic regression.
    Calculates the accuracy of the validation set to select the best parameters.
    """
    # Function classify() calculates conditional probability based on
    # self.bestParam. Therefore, for validation, it is required to set this to
    # W and b of this epoch.
    currBestParam = self.bestParam
    self.bestParam = (self.W, self.b)
    guesses = self.classify(validationData)
    n_correct = 0
    for expected, actual in zip(validationLabels, guesses):
      if expected == actual:
        n_correct += 1
    if n_correct > self.bestNCorrect:
      self.bestNCorrect = n_correct
    else:
      self.bestParam = currBestParam

  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.

    Do not modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      logposterior = self.calculateConditionalProbability(datum)
      guesses.append(np.argmax(logposterior))
      self.posteriors.append(logposterior)

    return guesses

  def calculateConditionalProbability(self, datum):
    """
    datum : D-sized numpy array
    - D : the number of features (PCA was used for feature extraction)
    RETURN : C-sized numpy array
    - C : the number of legal labels

    Returns the conditional probability p(y|x) to predict labels for the datum.
    Return value is NOT the log of probability, which means
    sum of your calculation should be 1. (sum_y p(y|x) = 1)
    """

    bestW, bestb = self.bestParam # These are parameters used for calculating conditional probabilities
    Wx = np.dot(datum, bestW)
    prob = [self.softmax(c, Wx, bestb) for c in self.legalLabels]
    return prob
