from math import exp
from ghmm import *
import ghmm

################################
#
#
# IGNORE THIS FILE
#
#
################################

def disable_ghmm_log():
    ghmm.c_log = [ (lambda *args: None) for i in xrange(len(ghmm.c_log)) ]

disable_ghmm_log()

# possible values
symbols = Alphabet("N E W S NE NW SE SW".split())
states_count = 8
per_symbol = 0.125
per_state = 0.125
# transition matrix
A = [ [ per_state for i in xrange(states_count) ] for j in xrange(states_count) ]    # 0.05 = 1/20

# emission matrix
B = [
    [ per_symbol or i in xrange(len(symbols)) ]
    for j in xrange(states_count)
]

# initial probabilities
# pi = [1.0] + [0.0]*(states_count-1)
pi = [ per_state for i in xrange(states_count) ]

m = HMMFromMatrices(symbols, DiscreteDistribution(symbols), A, B, pi)
# m = HMM()
# print m

training_set = [
        EmissionSequence(symbols, raw)
        for raw in [
            ["N"]*20 + ["E"]*10 + ["S"]*15,
            ["N"]*25 + ["E"]*3 + ["S"]*5,
            ["N"]*20 + ["E"]*12 + ["S"]*25,
            ["N"]*24 + ["E"]*8 + ["S"]*10,
            ["N"]*20 + ["E"]*10 + ["S"]*15,
            ["N"]*20 + ["E"]*10 + ["S"]*10,
            # ["N"]*20 + ["E"]*3 + ["NE", "NW", "SE", "SE", "NE"] + ["E"]*3 + ["S"]*13,
            # ["N"]*20 + ["E"]*10 + ["S"]*7 + ["SW", "SE", "SW"] + ["S"]*7,
            ["N"]*20 + ["E"]*10 + ["S"]*15,
            ["N"]*20 + ["E"]*10 + ["S"]*15,
            ["N"]*20 + ["E"]*10 + ["S"]*15
        ]
    #     for raw in [
    #     ["N"]*200 + ["E"]*100 + ["S"]*150,
    #     ["N"]*250 + ["E"]*30 + ["S"]*50,
    #     ["N"]*200 + ["E"]*120 + ["S"]*250,
    #     ["N"]*240 + ["E"]*80 + ["S"]*100,
    #     ["N"]*200 + ["E"]*100 + ["S"]*150,
    #     ["N"]*200 + ["E"]*100 + ["S"]*100,
    #     ["N"]*200 + ["E"]*30 + ["NE", "NW", "SE", "SE", "NE"]*10 + ["E"]*30 + ["S"]*130,
    #     ["N"]*200 + ["E"]*100 + ["S"]*70 + ["SW", "SE", "SW"]*10 + ["S"]*70,
    #     ["N"]*200 + ["E"]*100 + ["S"]*150
    # ]
    ]

for t in training_set:
    m.baumWelch(t)

print m

seq, log_p = m.viterbi(EmissionSequence(symbols, "N N N N N N N N N E E E E E E S S S S S S".split()))
print "most probable state sequence:", seq
print "log p:", log_p
print "p:", exp(log_p)
