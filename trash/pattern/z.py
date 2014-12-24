import numpy
from hmmlearn import hmm

def normalize_row(row):
    for k, v in {
        "X": 0,
        "N": 1,
        "NE": 2,
        "E": 3,
        "SE": 4,
        "S": 5,
        "SW": 6,
        "W": 7,
        "NW": 8
    }.iteritems():
        while k in row:
            row[row.index(k)] = v

def normalize_training_matrix(matrix):
    for row in matrix:
        normalize_row(row)

training_set = [
    ["N"]*20 + ["E"]*10 + ["S"]*15,
    ["N"]*25 + ["E"]*3 + ["S"]*5,
    ["N"]*20 + ["E"]*12 + ["S"]*25,
    ["N"]*24 + ["E"]*8 + ["S"]*10,
    ["N"]*20 + ["E"]*10 + ["S"]*15,
    ["N"]*20 + ["E"]*10 + ["S"]*10,
    ["N"]*20 + ["E"]*3 + ["NE", "NW", "SE", "SE", "NE"] + ["E"]*3 + ["S"]*13,
    ["N"]*20 + ["E"]*10 + ["S"]*7 + ["SW", "SE", "SW"] + ["S"]*7,
    ["N"]*20 + ["E"]*10 + ["S"]*15,
    ["N"]*20 + ["E"]*10 + ["S"]*15,
    ["N"]*20 + ["E"]*10 + ["S"]*15
]
max_length = len(max(training_set, key=len))
for t in training_set:
    t.extend(["X"]*(max_length-len(t)))
normalize_training_matrix(training_set)
training_set = numpy.array(training_set, numpy.int_)

model = hmm.GaussianHMM(9)
model.fit([training_set])

obs = ["N"]*15 + ["E"]*10 + ["S"]*3 + ["X"]*(max_length-28)
normalize_row(obs)

result = model.decode([obs], "viterbi")
print result

obs = ["N"]*25 + ["E"]*20 + ["S"]*10 + ["X"]*(max_length-55)
normalize_row(obs)

result = model.decode([obs], "viterbi")
print result

obs = ["N"]*25 + ["X"]*(max_length-25)
normalize_row(obs)

result = model.decode([obs], "viterbi")
print result

# works! result is pair (log_p, state_sequence)
# we ignore second one, and assume that high enough probability
# means that observation fits the model
# first and last are not enough to represent learned sequence, but second one is quite close

