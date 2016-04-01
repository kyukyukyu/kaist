# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 19:48:36 2016

@author: jmlee
"""
import itertools
import math
import sys
import classificationMethod
import numpy as np
import util

class GaussianDiscriminantAnalysisClassifier(classificationMethod.ClassificationMethod):
  def __init__(self, legalLabels, type):
    self.legalLabels = legalLabels
    self.type = type
    #: Function used for computing log joint probability. Used like
    #: logJointProbFunc(datum, y), where datum is a 1-D numpy array with
    #: features, and y is the label. Note that this is initialized with None
    #: at first.
    self.logJointProbFunc = None
    #: Shared precision matrix for LDA. Declared instead of covariance matrix
    #: since using precision matrix only is enough when computing log joint
    #: probabilities. Will be defined in trainAndTune().
    self.sharedPrecision = None
    #: Mapping from labels to their log priors. Also will be defined in
    #: trainAndTune().
    self.logPrior = dict()
    #: Mapping from labels to the mean vectors of instances with corresponding
    #: label. Also will be defined in trainAndTune().
    self.mean = dict()
    #: Mapping from labels to the precision matrices of instances with
    #: corresponding label. Declared for speed-up. Also will be defined in
    #: trainAndTune().
    self.precision = dict()
    #: Mapping from labels to the log constant in log joint probability
    #: formula for corresponding label based on QDA. Also will be defined in
    #: trainAndTune().
    self.qdaLogConstant = dict()

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method
    """
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels)

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Fill in this function!
    trainingData : (N x D)-sized numpy array
    validationData : (M x D)-sized numpy array
    trainingLabels : N-sized list
    validationLabels : M-sized list
    - N : the number of training instances
    - M : the number of validation instances
    - D : the number of features (PCA was used for feature extraction)

    Train the classifier by estimating MLEs.
    Evaluate LDA and QDA respectively and select the model that gives
    higher accuracy on the validationData.
    """
    #: Mapping of labels to the lists of instances with corresponding label.
    data = {label: [] for label in self.legalLabels}
    #: Mapping of labels to covariance matrices.
    covariance = dict()

    N, D = trainingData.shape

    # It turns out that the result of MLE for mean and covariance parameters of
    # each label are the mean and the covariance of training instances of each
    # label. Thus, group instances by their label and use these groups to
    # compute the label priors and mean and covariance of training instances of
    # each label.
    for tDatum, tLabel in zip(trainingData, trainingLabels):
      data[tLabel].append(tDatum)

    qdaCoeffBase = 1.0 / (2.0 * math.pi) ** (D / 2.0)
    for label, dataLabel in data.iteritems():
      nLabel = len(dataLabel)
      dataArray = np.array(dataLabel)
      logPrior = math.log(float(nLabel) / float(N))
      self.logPrior[label] = logPrior
      self.mean[label] = np.mean(dataArray, axis=0)
      covar = np.cov(dataArray, rowvar=0)
      covariance[label] = covar
      self.precision[label] = np.linalg.inv(covariance[label])
      self.qdaLogConstant[label] = (
        math.log(qdaCoeffBase / math.sqrt(np.linalg.det(covar))) +
        logPrior)
    # Calculate shared covariance and shared precision for LDA.
    sharedCovariance = np.average([covariance[l] for l in self.legalLabels],
                                  axis=0,
                                  weights=[len(data[l]) for l
                                                        in self.legalLabels])
    self.sharedPrecision = np.linalg.inv(sharedCovariance)

    # Try LDA and QDA once for each.
    self.logJointProbFunc = self.calcLogJointProbLDA
    guessesLDA = self.classify(validationData)
    accuracyLDA = self.calcAccuracy(validationLabels, guessesLDA)
    self.logJointProbFunc = self.calcLogJointProbQDA
    guessesQDA = self.classify(validationData)
    accuracyQDA = self.calcAccuracy(validationLabels, guessesQDA)
    if accuracyLDA >= accuracyQDA:
      self.logJointProbFunc = self.calcLogJointProbLDA
    else:
      self.logJointProbFunc = self.calcLogJointProbQDA

  @staticmethod
  def calcAccuracy(expectedLabels, actualLabels):
    if len(expectedLabels) != len(actualLabels):
      raise ValueError('Two lists of labels have different length')
    nCorrect = 0
    for el, al in itertools.izip(expectedLabels, actualLabels):
      if el == al:
        nCorrect += 1
    return float(nCorrect) / float(len(expectedLabels))

  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.

    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      logposterior = self.calculateLogJointProbabilities(datum)
      guesses.append(np.argmax(logposterior))
      self.posteriors.append(logposterior)

    return guesses

  def calculateLogJointProbabilities(self, datum):
    """
    datum: D-sized numpy array
    - D : the number of features (PCA was used for feature extraction)

    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the list, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    """
    logJoint = [self.logJointProbFunc(datum, c) for c in self.legalLabels]
    return logJoint

  def calcLogJointProbLDA(self, datum, y):
    """
    Calculates log joint probability of given datum and label using LDA model.
    """

    logPi = self.logPrior[y]
    mu = self.mean[y]
    lmda = self.sharedPrecision
    beta = np.dot(lmda, mu)
    gamma = -0.5 * np.dot(np.dot(mu, lmda), mu) + logPi
    return (np.dot(beta, datum) + gamma)

  def calcLogJointProbQDA(self, datum, y):
    """
    Calculates log joint probability of given datum and label using QDA model.
    """

    mu = self.mean[y]
    lmda = self.precision[y]
    logConstant = self.qdaLogConstant[y]
    z = datum - mu
    return (logConstant + (-0.5 * np.dot(np.dot(z, lmda), z)))
