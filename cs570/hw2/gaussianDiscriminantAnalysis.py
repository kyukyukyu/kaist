# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 19:48:36 2016

@author: jmlee
"""
import sys
import classificationMethod
import numpy as np
import util

class GaussianDiscriminantAnalysisClassifier(classificationMethod.ClassificationMethod):
  def __init__(self, legalLabels, type):
    self.legalLabels = legalLabels
    self.type = type
    #: Function used for computing log joint probability. Used like
    #: logJointProbFunc(data), where data is (N x D)-sized numpy array, N is the
    #: number of instances, and D is the number of features. Note that this is
    #: initialized with None at first.
    self.logJointProbFunc = None
    #: Covariance matrix for all of training instances. Will be defined in
    #: trainAndTune().
    self.totalCovariance = None
    #: Precision matrix for all of training instances. Declared for speed-up.
    #: Also will be defined in trainAndTune().
    self.totalPrecision = None
    #: Mapping from labels to their priors. Also will be defined in
    #: trainAndTune().
    self.prior = dict()
    #: Mapping from labels to the mean vectors of instances with corresponding
    #: label. Also will be defined in trainAndTune().
    self.mean = dict()
    #: Mapping from labels to the covariance matrices of instances with
    #: corresponding label. Also will be defined in trainAndTune().
    self.covariance = dict()
    #: Mapping from labels to the precision matrices of instances with
    #: corresponding label. Declared for speed-up. Also will be defined in
    #: trainAndTune().
    self.precision = dict()

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

    N = trainingData.shape[0]
    self.totalCovariance = np.cov(trainingData, rowvar=0)
    self.totalPrecision = self.totalCovariance.T

    # It turns out that the result of MLE for mean and covariance parameters of
    # each label are the mean and the covariance of training instances of each
    # label. Thus, group instances by their label and use these groups to
    # compute the label priors and mean and covariance of training instances of
    # each label.
    for tDatum, tLabel in zip(trainingData, trainingLabels):
      data[tLabel].append(tDatum)
    for label, dataLabel in data.iteritems():
      self.prior[label] = float(len(dataLabel)) / float(N)
      self.mean[label] = np.mean(dataLabel, axis=0)
      self.covar[label] = np.cov(dataLabel, rowvar=0)
      self.precision[label] = self.covar[label].T

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
    logJoint = [0 for c in self.legalLabels]

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
    return logJoint
