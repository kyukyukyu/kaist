# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 2016

@author: bjlee
"""
import classificationMethod
import numpy as np
import scipy.linalg
import sys
import util
linalg_solve = np.linalg.solve

def softmax(X):
    e = np.exp(X - np.max(X))
    det = np.sum(e, axis=1)
    return (e.T / det).T

class gaussianProcessClassifier(classificationMethod.ClassificationMethod):
    def __init__(self, legalLabels, type, seed, data):
        self.legalLabels = legalLabels
        self.numpRng = np.random.RandomState(seed)
        self.numberofsamples = 1000
        self.data = data

    def initializeHyp(self):
        """
        Initialize hyper-parameter appropriately

        Do not modify this method.
        """
        self.trainingShape = np.shape(self.trainingData)
        [n,d] = self.trainingShape
        c = len(self.legalLabels)
        if self.data == 'faces':
            noise = 250.0
        else:
            noise = 20.0
        self.hypSize = [c, 2]
        self.hyp = np.zeros(self.hypSize)
        for i in range(c):
            self.hyp[i,:] = np.array([np.log(noise)/2, np.log(noise/4)/2])


    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        You may commentize or decommentize few lines here to change the behavior of the program
        """

        self.trainingData = trainingData
        self.trainingLabels = trainingLabels
        self.initializeHyp()

        """
        Decommentize the line below to check whether the implementation is correct:

        This method compares the gradient computed by method 'derivative_of_marginalLikelihood'

        with the finite difference of method 'marginalLikelihood'.

        If the final output of 'checkGradient' method is very small (less than 1e-4),

        your implementation on method 'marginalLikelihood' may be right.
        """
        #self.checkGradient(1e-4)

        """
        The three lines below optimizes the marginal likelihood with conjugate gradient algorithm.

        Since I initialized hyper-parameters with appropriate values, the algorithm would do well without optimization;

        decommentize theses lines if you are curious.

        Note: optimization with digit dataset may not work due to the numerical issue
        """
        #print "initial hyp: ", self.hyp.ravel()
        #print "initial negative approx. marginal likelihood: ", self.marginalLikelihood(self.hyp)
        #res = sp.optimize.minimize(self.marginalLikelihood, self.hyp, method='CG'\
        #    , jac=self.derivative_of_marginalLikelihood, options = {'maxiter':25})
        #self.hyp = np.reshape(res.x, self.hypSize)
        #print res

    def calculateIntermediateValues(self, t, a, Kcs):
        [n,d] = self.trainingShape
        C = len(self.legalLabels)
        # Flatten t and a into 1D array.
        t = t.flatten()
        a = a.flatten()
        # Compute pi from a.
        exp_a = np.exp(a).reshape([-1, n])
        pi = (exp_a / np.sum(exp_a, 0)).flatten()
        # Compute K.
        K = scipy.linalg.block_diag(*Kcs)
        # Compute D.
        D = np.diagflat(pi)
        # Compute M, E, and logdet.
        logdet = 0
        Ecs = [None] * C
        for c in self.legalLabels:
            cn = c * n
            D_c = D[cn:(cn + n), cn:(cn + n)]
            K_c = Kcs[c]
            sqrt_D_c = scipy.linalg.sqrtm(D_c)
            I_n = np.identity(n)
            L = np.linalg.cholesky(I_n + np.dot(np.dot(sqrt_D_c, K_c),
                                                sqrt_D_c))
            Ecs[c] = np.dot(sqrt_D_c, linalg_solve(L.T,
                                                   linalg_solve(L, sqrt_D_c)))
            logdet += np.sum(np.log(np.diag(L)))
        M = np.linalg.cholesky(np.sum(Ecs, axis=0))
        E = scipy.linalg.block_diag(*Ecs)
        logdet += np.sum(np.log(np.diag(M)))
        # Compute Pi.
        Pi = np.dot(D, np.tile(np.identity(n), (C, 1)))
        # Compute W.
        W = D - np.dot(Pi, Pi.T)
        # Compute R.
        R = np.dot(np.linalg.inv(D), Pi)
        # Compute b.
        c = np.dot(W, a) + t - pi
        d = np.dot(np.dot(E, K), c)
        ER = np.dot(E, R)
        b = c - d + np.dot(ER, linalg_solve(M.T,
                                            linalg_solve(M, np.dot(R.T, d))))
        # Reshape 1D array variables.
        b = b.reshape((-1, 1))
        pi = pi.reshape((-1, 1))
        valuesForModes = [W, b, logdet, K]
        valuesForDerivatives = [E, M, R, b, pi, K]
        valuesForPrediction = [pi, Ecs, M, R, K]
        return valuesForModes, valuesForDerivatives, valuesForPrediction

    def findMode(self, trainingData, trainingLabels, hyp):
        [n,d] = self.trainingShape
        c = len(self.legalLabels)

        Kcs = self.calculateCovariance(trainingData, hyp)
        [t,_] = self.trainingLabels2t(trainingLabels)
        t_ = t.flatten()

        a = np.zeros_like(t)
        objective_old = None
        logdet = 0.0
        while True:
            ((_, b, logdet, K), _, _) = self.calculateIntermediateValues(t, a,
                                                                         Kcs)
            a = np.dot(K, b)
            # Flatten b and a for convenience.
            b = b.flatten()
            a = a.flatten()
            exp_a_reshaped = np.exp(a).reshape((c, -1))
            exp_a_logsums = np.log(np.sum(exp_a_reshaped, 1))
            summed_term = np.sum(exp_a_logsums)
            objective = -0.5 * np.dot(b, a) + np.dot(t_, a) - summed_term
            if objective_old is not None and np.isclose(objective,
                                                        objective_old):
                break
            objective_old = objective
        Z = objective - logdet

        return a, Z

    def calculatePredictiveDistribution(self, datum, pi, Ecs, M, R, tc):
        datum_reshaped = datum.reshape([1, -1])
        trainingData = self.trainingData
        legalLabels = self.legalLabels
        C = len(legalLabels)
        (n, d) = self.trainingShape
        # Compute k_(c, n + 1).
        k_news = [self.covARD(self.hyp[c], trainingData, datum_reshaped)
                  for c in legalLabels]
        k_news = np.array(k_news).reshape((C, n))
        # Compute k_(c, n + 1, n + 1).
        k_new_news = [self.covARD(self.hyp[c], datum_reshaped)[0]
                      for c in legalLabels]
        # Compute R_c by splitting R. This is a list of C n x n arrays.
        Rcs = [R[(c * n):(c * n + n), :] for c in legalLabels]
        # Split pi by labels. The shape of this array should be (C, n).
        pi_cs = pi.reshape([-1, n])
        # Compute latent test mean. This is equal to extracting diagonal
        # elements from np.dot(k_news, tc - pi_cs.T) while eliminating
        # needless computations. Source: http://stackoverflow.com/a/14759273
        mu = np.einsum('ij,ji->i', k_news, tc - pi_cs.T)
        # Compute latent test covariance.
        sigma = np.zeros([C, C])
        for c in legalLabels:
            Ec = Ecs[c]
            k_new_c = k_news[c]
            Rc = Rcs[c]
            f = np.dot(Ec, k_new_c)
            # g := Ec * (Rc * (M.T \ (M \ (Rc.T * f))))
            g = np.dot(Ec,
                       np.dot(Rc,
                              linalg_solve(M.T,
                                           linalg_solve(M, np.dot(Rc.T, f)))))
            sigma[c] = np.dot(k_news, g)
            sigma[c, c] += k_new_news[c] - np.dot(f, k_new_c)
        # MC estimate of prediction vector.
        samples = self.numpRng.multivariate_normal(mu.ravel(),sigma,self.numberofsamples)
        predict = softmax(samples)
        return np.mean(predict,0)

    def derivative_of_marginalLikelihood(self, hyp):
        """
        This method calculates the derivative of marginal likelihood.

        You may refer to this code to see what methods in numpy is useful

        while you are implementing other functions.

        Do not modify this method.
        """
        trainingData = self.trainingData
        trainingLabels = self.trainingLabels
        c = len(self.legalLabels)
        [n,d] = self.trainingShape
        hyp = np.reshape(hyp, self.hypSize)

        [mode,_] = self.findMode(trainingData, trainingLabels, hyp)
        [t,_] = self.trainingLabels2t(trainingLabels)

        Ks = self.calculateCovariance(trainingData, hyp)
        [_,[E, M, R, b, totpi, K],_] = self.calculateIntermediateValues(t, mode, Ks)

        MRE = np.linalg.solve(M,R.T.dot(E))
        MMRE = np.linalg.solve(M.T,MRE)
        KWinvinv = E-E.dot(R.dot(MMRE))

        KinvWinv = K-K.dot(KWinvinv.dot(K))
        partitioned_KinvWinv = np.transpose(np.array(np.split(np.array(np.split(KinvWinv, c)),c,2)),[2,3,1,0])

        s2 = np.zeros([n,c])
        for i in range(n):
            pi_n = softmax(np.reshape(mode,[c,n])[:,i:i+1].T).T
            pipj = pi_n.dot(pi_n.T)
            pi_3d = np.zeros([c,c,c])
            pi_3d[np.diag_indices(c,3)] = pi_n.ravel()
            pipjpk = np.tensordot(pi_n,np.reshape(pipj,(1,c,c)),(1,0))
            pipj_3d = np.zeros([c,c,c])
            pipj_3d[np.diag_indices(c)] = pipj
            W_3d = pi_3d + 2 * pipjpk - pipj_3d - np.transpose(pipj_3d,[2,1,0]) - np.transpose(pipj_3d,[1,2,0])
            s2[i,:] = -0.5*np.trace(partitioned_KinvWinv[i,i].dot(W_3d))

        b_rs = np.reshape(b, [c,n])
        dZ = np.zeros(hyp.shape)
        for j in range(2):
            cs = []
            zeroCs = [np.zeros([n,n]) for i in range(c)]
            for i in range(c):
                C = self.covARD(hyp[i,:],trainingData,None,j)
                dZ[i,j] = 0.5*b_rs[i,:].T.dot(C.dot(b_rs[i,:]))
                zeroCs[i] = C
                cs.append(self.block_diag(zeroCs))
                zeroCs[i] = np.zeros([n,n])

            for i in range(c):
                dd = cs[i].dot(t-totpi)
                s3 = dd - K.dot(KWinvinv.dot(dd))
                dZ[i,j] +=  - 0.5 * np.trace(KWinvinv.dot(cs[i])) + s2.T.ravel().dot(s3) #

        return -dZ.ravel()

    def marginalLikelihood(self, hyp):
        """
        Wrapper function for scipy.optimize:

        Do not modify this method.
        """
        trainingData = self.trainingData
        trainingLabels = self.trainingLabels
        hyp = np.reshape(hyp, self.hypSize)

        [_, Z] = self.findMode(trainingData, trainingLabels, hyp)
        return -Z

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        Do not modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).

        [mode,_] = self.findMode(self.trainingData, self.trainingLabels, self.hyp)
        Kcs = self.calculateCovariance(self.trainingData, self.hyp)
        [t,tc] = self.trainingLabels2t(self.trainingLabels)
        [_,_,[pi, Ecs, M, R, K]] = self.calculateIntermediateValues(t, mode, Kcs)

        for datum in testData:
          logposterior = self.calculatePredictiveDistribution(datum, pi, Ecs, M, R, tc)
          guesses.append(np.argmax(logposterior))
          self.posteriors.append(logposterior)

        print guesses
        return guesses


    def checkGradient(self, error):
        """
        Method to check whether the gradient is right by comparing with finite difference.

        Since I give you the right gradient function, you may use this to check

        whether the marginal likelihood implementation is right.
        """
        hyp = self.hyp
        c = len(self.legalLabels)
        [n,d] = self.trainingShape
        dh = np.zeros(hyp.shape)
        dZ = np.reshape(self.derivative_of_marginalLikelihood(hyp),self.hypSize)
        for i in range(c):
            for j in range(2):
                print (i,j)
                ehyp = np.copy(hyp)
                ehyp[i,j] += error
                Z2 = self.marginalLikelihood(ehyp)
                ehyp[i,j] -= error * 2
                Z3 = self.marginalLikelihood(ehyp)
                dh[i,j] = (Z2-Z3) / (2 * error)
        print dZ
        print dh
        print (dh-dZ)/(dh+dZ)


    def covARD(self, hyp, x, z = None, i = None):
        """
         Squared Exponential covariance function with isotropic distance measure. The
         covariance function is parameterized as:

         k(x^p,x^q) = sf^2 * exp(-(x^p - x^q)'*inv(P)*(x^p - x^q)/2)

         where the P matrix is ell^2 times the unit matrix and sf^2 is the signal
         variance. The hyperparameters are:
         hyp = [ log(ell)
                 log(sf)  ]

        """
        def sq_dist(a, b = None):
            [D, n] = np.shape(a)
            if b is None:
                mu = np.mean(a,1)
                a = (a.T - mu).T
                b = a
                m = n
            else:
                [d, m] = np.shape(b)
                if d != D:
                    print 'Error: column lengths must agree.'
                    sys.exit(1)
                mu = (m/(n+m))*np.mean(b,1) + (n/(n+m))*np.mean(a,1)
                a = (a.T - mu).T
                b = (b.T - mu).T
            return np.tile(np.sum(a*a, 0), [m, 1]).T + np.tile(np.sum(b*b, 0), [n, 1]) - 2 * a.T.dot(b)

        xeqz = z is None
        ell = np.exp(hyp[0])
        sf2 = np.exp(2 * hyp[1])
        if xeqz:
            K = sq_dist(x.T/ell)
        else:
            K = sq_dist(x.T/ell,z.T/ell)
        if i is not None:
            if i == 0:
                K = sf2 * np.exp(-K/2) * K
            elif i == 1:
                K = 2 * sf2 * np.exp(-K/2)
            else:
                print 'Unkown parameter!'
                sys.exit(1)
        else:
            K = sf2 * np.exp(-K/2)
        return K



    def calculateCovariance(self, trainingData, hyp):
        Ks = []
        c = len(self.legalLabels)
        for i in range(c):
            Ks.append(self.covARD(hyp[i,:],trainingData))
        return Ks

    def trainingLabels2t(self, trainingLabels):
        t = []
        n = np.shape(trainingLabels)[0]
        c = len(self.legalLabels)
        for i in range(n):
            temp = np.zeros([c,1])
            temp[trainingLabels[i]] = 1
            t.append(temp)
        ttot = np.concatenate(t)
        tc = np.reshape(ttot,[n,c])
        ttot = np.reshape(tc.T,[n*c,1])

        return ttot, tc

    def block_diag(self, args):
        return scipy.linalg.block_diag(*args)
