from math import exp
from ghmm import *



sigma = IntegerRange(1,7)
A = [[0.9, 0.1], [0.3, 0.7]]
efair = [1.0 / 6] * 6
eloaded = [3.0 / 13, 3.0 / 13, 2.0 / 13, 2.0 / 13, 2.0 / 13, 1.0 / 13]
B = [efair, eloaded]
pi = [0.5] * 2
m = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
# print m


seq, p = m.viterbi(EmissionSequence(sigma, [1, 5, 3]))
print "most probable state sequence:", seq
print "probability:", exp(p)