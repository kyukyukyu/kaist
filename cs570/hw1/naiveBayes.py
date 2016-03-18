from functools import reduce
import itertools
import math

import classificationMethod
import util


class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.

  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    #: List of features in data. Initialized in train().
    self.features = None
    #: List of log posteriors for test data, stored for grading. Initialized in
    #: classify().
    self.posteriors = None
    #: Counter of labels of training instances. i.e. c(y). cntLabel[y] is the
    #: number of instances whose label is y.
    self.cntLabel = util.Counter()
    #: Counter of features and labels of training instances. i.e. c(f_i, y).
    #: cntFeatLabel[(feat, y)] is the number of instances whose value of feat is
    #: 1 and label is y.
    self.cntFeatLabel = util.Counter()

  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """

    self.features = trainingData[0].keys() # this could be useful for your code later...

    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]

    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter
    that gives the best accuracy on the held-out validationData.

    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    for tDatum, tLabel in itertools.izip(trainingData, trainingLabels):
      assert tLabel in self.legalLabels
      self.cntLabel[tLabel] += 1
      for fKey, fValue in tDatum.iteritems():
        if 1 == fValue:
          self.cntFeatLabel[(fKey, tLabel)] += 1

    # Find the best smoothing parameter.
    max_accuracy = 0.0
    max_k = 0
    nValidationData = len(validationData)
    assert nValidationData > 0
    for k in kgrid:
        self.setSmoothing(k)
        guesses = self.classify(validationData)
        nCorrect = reduce(lambda n, lp: n + (1 if lp[0] == lp[1] else 0),
                          itertools.izip(validationLabels, guesses),
                          0)
        accuracy = float(nCorrect) / float(nValidationData)
        if max_accuracy < accuracy:
            max_accuracy = accuracy
            max_k = k
    self.setSmoothing(max_k)

  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.

    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses

  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    """
    logJoint = util.Counter()

    # P(Label = y, datum)
    #   = P(Label = y) * P(datum | Label = y) (by Bayes rule)
    #   = P(Label = y) * P(F_1 = f_1 | Label = y) * P(F_2 = f_2 | Label = y) *
    #                    ... * P(F_D = f_D | Label = y) (conditional indep.)
    #   = (n_y / n) * ((c(f_1, y) + k) / (n_y + 2 * k)) *
    #                 ((c(f_2, y) + k) / (n_y + 2 * k)) *
    #                 ... *
    #                 ((c(f_D, y) + k) / (n_y + 2 * k))
    #     (There are only two possible values for one feature. Thus, 2 * k.)
    #
    # where n is the number of instances in training set,
    # n_y is the number of instances with label y in training set,
    # c(f_i, y) is the number of instances whose value of feature F_i is f_i and
    # label is y in training set,
    # D is the number of features in a datum, ('D' from 'dimension')
    # and k is smoothing parameter.
    #
    # Hence, in log-probability,
    #
    # log(P(Label = y, datum))
    #   = log(n_y / n) + log(c(f_1, y) + k) + log(c(f_2, y) + k) + ... +
    #     log(c(f_D, y) + k) - D * log(n_y + 2 * k)
    n = float(self.cntLabel.totalCount())
    d = len(self.features)
    k = self.k
    for y in self.legalLabels:
      n_y = self.cntLabel[y]
      logPrior = math.log(float(n_y) / n)
      logCounts = 0
      for f in self.features:
        counts = 0
        if 1 == datum[f]:
          counts = self.cntFeatLabel[(f, y)]
        else:
          counts = n_y - self.cntFeatLabel[(f, y)]
        logCounts += math.log(counts + k)
      logJoint[y] = logPrior + logCounts - d * math.log(n_y + k + k)

    return logJoint
