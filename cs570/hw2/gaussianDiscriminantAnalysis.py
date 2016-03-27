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

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


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
