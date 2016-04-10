# This file contains feature extraction methods and harness 
# code for data classification

import mostFrequent
import naiveBayes
import gaussianDiscriminantAnalysis
import logisticRegression
import samples
import sys
import util
import numpy as np
import cPickle

TEST_SET_SIZE = 100
DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28
FACE_DATUM_WIDTH=60
FACE_DATUM_HEIGHT=70


def basicFeatureExtractorDigit(datum):
  """
  Returns a set of pixel features indicating whether
  each pixel in the provided datum is white (0) or gray/black (1)
  """
  features = util.Counter()
  for x in range(DIGIT_DATUM_WIDTH):
    for y in range(DIGIT_DATUM_HEIGHT):
      if datum.getPixel(x, y) > 0:
        features[(x,y)] = 1
      else:
        features[(x,y)] = 0
  return features

def basicFeatureExtractorFace(datum):
  """
  Returns a set of pixel features indicating whether
  each pixel in the provided datum is an edge (1) or no edge (0)
  """
  features = util.Counter()
  for x in range(FACE_DATUM_WIDTH):
    for y in range(FACE_DATUM_HEIGHT):
      if datum.getPixel(x, y) > 0:
        features[(x,y)] = 1
      else:
        features[(x,y)] = 0
  return features
  
def basicFeatureDataToNumpyArray(basicFeatureData):
  """
  Convert basic feature data(Counter) to N x d numpy array
  """
  N = len(basicFeatureData)
  D = len(basicFeatureData[0])
  keys = basicFeatureData[0].keys()

  data = np.zeros((N, D))
  for i in range(N):
    for j in range(D):
      data[i][j] = basicFeatureData[i][keys[j]]
      
  #data_std = np.std(data, 0)
  #mask = data_std == 0
  #data = data[:, ~mask]
  
  return data

def getPrincipleComponents(basicFeatureData, pc_count):
  """
  Returns top-k principle components for dimensionality reduction (PCA)
  """
  data = basicFeatureDataToNumpyArray(basicFeatureData)

  data -= np.mean(data, 0) # mean centering
  C = np.cov(data.T)
  E, V = np.linalg.eigh(C)
  key = np.argsort(E)[::-1][:pc_count]
  E, V = E[key], V[:, key]

  return V # V: top-k eigenvectors

def analysis(classifier, guesses, testLabels, testData, rawTestData, printImage):
  """
  This function is called after learning.
  Include any code that you want here to help you analyze your results.
  
  Use the printImage(<list of pixels>) function to visualize features.
  
  An example of use has been given to you.
  
  - classifier is the trained classifier
  - guesses is the list of labels predicted by your classifier on the test set
  - testLabels is the list of true labels
  - testData is the list of training datapoints (as util.Counter of features)
  - rawTestData is the list of training datapoints (as samples.Datum)
  - printImage is a method to visualize the features 
  
  This code won't be evaluated. It is for your own optional use
  (and you can modify the signature if you want).
  """
  
  # Put any code here...
  # Example of use:
  for i in range(len(guesses)):
      prediction = guesses[i]
      truth = testLabels[i]
      if (prediction != truth):
          print "==================================="
          print "Mistake on example %d" % i 
          print "Predicted %d; truth is %d" % (prediction, truth)
          print "Image: "
          print rawTestData[i]
          break


## =====================
## You don't have to modify any code below.
## =====================


class ImagePrinter:
    def __init__(self, width, height):
      self.width = width
      self.height = height

    def printImage(self, pixels):
      """
      Prints a Datum object that contains all pixels in the 
      provided list of pixels.  This will serve as a helper function
      to the analysis function you write.
      
      Pixels should take the form 
      [(2,2), (2, 3), ...] 
      where each tuple represents a pixel.
      """
      image = samples.Datum(None,self.width,self.height)
      for pix in pixels:
        try:
            # This is so that new features that you could define which 
            # which are not of the form of (x,y) will not break
            # this image printer...
            x,y = pix
            image.pixels[x][y] = 2
        except:
            print "new features:", pix
            continue
      print image  

def default(str):
  return str + ' [Default: %default]'

def readCommand( argv ):
  "Processes the command used to run from the command line."
  from optparse import OptionParser  
  parser = OptionParser(USAGE_STRING)
  
  parser.add_option('-c', '--classifier', help=default('The type of classifier'), choices=['mostFrequent', 'nb', 'naiveBayes', 'GDA', 'logisticRegression', 'lr'], default='mostFrequent')
  parser.add_option('-d', '--data', help=default('Dataset to use'), choices=['digits', 'faces'], default='digits')
  parser.add_option('-t', '--training', help=default('The size of the training set'), default=450, type="int")
  parser.add_option('-k', '--smoothing', help=default("Smoothing parameter (ignored when using --autotune)"), type="float", default=2.0)
  parser.add_option('-a', '--autotune', help=default("Whether to automatically tune hyperparameters"), default=False, action="store_true")
  parser.add_option('-i', '--iterations', help=default("Maximum iterations to run training"), default=3, type="int")

  options, otherjunk = parser.parse_args(argv)
  if len(otherjunk) != 0: raise Exception('Command line input not understood: ' + str(otherjunk))
  args = {}
  
  # Set up variables according to the command line input.
  print "Doing classification"
  print "--------------------"
  print "data:\t\t" + options.data
  print "classifier:\t\t" + options.classifier
  print "training set size:\t" + str(options.training)
  if(options.data=="digits"):
    printImage = ImagePrinter(DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT).printImage
    featureFunction = basicFeatureExtractorDigit
  elif(options.data=="faces"):
    printImage = ImagePrinter(FACE_DATUM_WIDTH, FACE_DATUM_HEIGHT).printImage
    featureFunction = basicFeatureExtractorFace
  else:
    print "Unknown dataset", options.data
    print USAGE_STRING
    sys.exit(2)
    
  if(options.data=="digits"):
    legalLabels = range(10)
  else:
    legalLabels = range(2)

  if options.training <= 0:
    print "Training set size should be a positive integer (you provided: %d)" % options.training
    print USAGE_STRING
    sys.exit(2)
    
  if options.smoothing <= 0:
    print "Please provide a positive number for smoothing (you provided: %f)" % options.smoothing
    print USAGE_STRING
    sys.exit(2)
    
  if(options.classifier == "mostFrequent"):
    classifier = mostFrequent.MostFrequentClassifier(legalLabels)
  elif(options.classifier == "naiveBayes" or options.classifier == "nb"):
    classifier = naiveBayes.NaiveBayesClassifier(legalLabels)
    classifier.setSmoothing(options.smoothing)
    if (options.autotune):
        print "using automatic tuning for naivebayes"
        classifier.automaticTuning = True
    else:
        print "using smoothing parameter k=%f for naivebayes" %  options.smoothing
  elif(options.classifier == "GDA"):
    classifier = gaussianDiscriminantAnalysis.GaussianDiscriminantAnalysisClassifier(legalLabels, "GDA")
  elif(options.classifier == "logisticRegression" or options.classifier == "lr"):
    classifier = logisticRegression.LogisticRegressionClassifier(legalLabels, "LogisticRegression", 123)
    options.classifier = "LR"
  else:
    print "Unknown classifier:", options.classifier
    print USAGE_STRING
    
    sys.exit(2)

  args['classifier'] = classifier
  args['featureFunction'] = featureFunction
  args['printImage'] = printImage
  
  return args, options

USAGE_STRING = """
  USAGE:      python dataClassifier.py <options>
  EXAMPLES:   (1) python dataClassifier.py
                  - trains the default mostFrequent classifier on the digit dataset
                  using the default 100 training examples and
                  then test the classifier on test data
              (2) python dataClassifier.py -c naiveBayes -d digits -t 1000 -k 2.5
                  - would run the naive Bayes classifier on 1000 training examples
                  using the smoothing parameter equals to 2.5
                 """

# Main harness code

def runClassifier(args, options):

  featureFunction = args['featureFunction']
  classifier = args['classifier']
  printImage = args['printImage']
      
  # Load data  
  numTraining = options.training

  # Extract features
  print "Extracting features..."
  if options.data=="faces":
    rawTrainingData = samples.loadDataFile("facedata/facedatatrain", numTraining,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)
    trainingLabels  = samples.loadLabelsFile("facedata/facedatatrainlabels", numTraining)
    rawValidationData = samples.loadDataFile("facedata/facedatavalidation", TEST_SET_SIZE,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)
    validationLabels  = samples.loadLabelsFile("facedata/facedatavalidationlabels", TEST_SET_SIZE)
    rawTestData = samples.loadDataFile("facedata/facedatatest", TEST_SET_SIZE,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)
    testLabels  = samples.loadLabelsFile("facedata/facedatatestlabels", TEST_SET_SIZE)
  else:
    rawTrainingData = samples.loadDataFile("digitdata/trainingimages", numTraining,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
    trainingLabels = samples.loadLabelsFile("digitdata/traininglabels", numTraining)
    rawValidationData = samples.loadDataFile("digitdata/validationimages", TEST_SET_SIZE,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
    validationLabels = samples.loadLabelsFile("digitdata/validationlabels", TEST_SET_SIZE)
    rawTestData = samples.loadDataFile("digitdata/testimages", TEST_SET_SIZE,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
    testLabels = samples.loadLabelsFile("digitdata/testlabels", TEST_SET_SIZE)

  if options.classifier == "GDA" or options.classifier == "LR":
    import os.path
    if os.path.isfile(options.data + '_' + str(numTraining) + '_pca.np'):
      f = open(options.data + '_' + str(numTraining) + '_pca.np', 'rb')
      principleComponents, trainingData, validationData, testData = cPickle.load(f) 
      f.close()
    else:
      if options.data == "faces":
        dimension = 13
        principleComponents = getPrincipleComponents(map(featureFunction, samples.loadDataFile("facedata/facedatatrain",451,FACE_DATUM_WIDTH,FACE_DATUM_HEIGHT)), dimension)
        trainingData = np.dot(basicFeatureDataToNumpyArray(map(featureFunction, rawTrainingData)), principleComponents)
        validationData = np.dot(basicFeatureDataToNumpyArray(map(featureFunction, rawValidationData)), principleComponents)
        testData = np.dot(basicFeatureDataToNumpyArray(map(featureFunction, rawTestData)), principleComponents)
      else:
        dimension = 13
        principleComponents = getPrincipleComponents(map(featureFunction, samples.loadDataFile("digitdata/trainingimages",5000,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)), dimension)
        trainingData = np.dot(basicFeatureDataToNumpyArray(map(featureFunction, rawTrainingData)), principleComponents)
        validationData = np.dot(basicFeatureDataToNumpyArray(map(featureFunction, rawValidationData)), principleComponents)
        testData = np.dot(basicFeatureDataToNumpyArray(map(featureFunction, rawTestData)), principleComponents)
      f = open(options.data + '_' + str(numTraining) + '_pca.np', 'wb')
      cPickle.dump((principleComponents, trainingData, validationData, testData), f)
      f.close()
  else:
    trainingData = map(featureFunction, rawTrainingData)
    validationData = map(featureFunction, rawValidationData)
    testData = map(featureFunction, rawTestData)

  # Conduct training and testing
  print "Training..."
  classifier.train(trainingData, trainingLabels, validationData, validationLabels)
  print "Validating..."
  guesses = classifier.classify(validationData)
  correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
  print str(correct), ("correct out of " + str(len(validationLabels)) + " (%.1f%%).") % (100.0 * correct / len(validationLabels))
  print "Testing..."
  guesses = classifier.classify(testData)
  correct = [guesses[i] == testLabels[i] for i in range(len(testLabels))].count(True)
  print str(correct), ("correct out of " + str(len(testLabels)) + " (%.1f%%).") % (100.0 * correct / len(testLabels))
  analysis(classifier, guesses, testLabels, testData, rawTestData, printImage)
  

if __name__ == '__main__':
  # Read input  
  args, options = readCommand( sys.argv[1:] ) 
  # Run classifier
  runClassifier(args, options)
