from math import exp
from ghmm import *


# possible values
sigma = IntegerRange(1,7)
# transition matrix
A = [[0.9, 0.1], [0.3, 0.7]]

efair = [1.0 / 6] * 6
eloaded = [3.0 / 13, 3.0 / 13, 2.0 / 13, 2.0 / 13, 2.0 / 13, 1.0 / 13]
# emission matrix
B = [efair, eloaded]
# initial probabilities
pi = [0.5] * 2
m = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
# print m


# seq, p = m.viterbi(EmissionSequence(sigma, [1, 5, 3]))
seq, p = m.viterbi(EmissionSequence(sigma, [1] * 20 + [6] * 10 + [1] * 40))
print "most probable state sequence:", seq
print "probability:", p, exp(p)