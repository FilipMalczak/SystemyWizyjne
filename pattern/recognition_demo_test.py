import os
from pattern.recognition import Recognizer

dumpfile = os.path.join(os.path.dirname(__file__), "example.recognizer")

r = Recognizer(dumpfile, range(9))

training_set = [
    [1]*20 + [3]*10 + [5]*15,
    [1]*25 + [3]*3 + [5]*5,
    [1]*20 + [3]*12 + [5]*25,
    [1]*24 + [3]*8 + [5]*10,
    [1]*20 + [3]*10 + [5]*15,
    [1]*20 + [3]*10 + [5]*10,
    [1]*20 + [3]*3 + [2, 8, 4, 4, 2] + [3]*3 + [5]*13,
    [1]*20 + [3]*10 + [5]*7 + [3, 4, 7] + [5]*7,
    [1]*20 + [3]*10 + [5]*15,
    [1]*20 + [3]*10 + [5]*15,
    [1]*20 + [3]*10 + [5]*15
]

r.learn("NES", *training_set)

training_set = [
    [2]* 7 + [3]*5 + [4] + [3]*5 + [4]*8 + [5]*12 + [6]*20 + [7]*18 + [8]*8 + [1]*10,
    [2]* 8 + [3]*5 + [4]*8 + [5]*12 + [6]*20 + [7]*18 + [8]*8 + [1]*3,
    [2]* 8 + [3]*3 + [4]*8 + [5]*20 + [6]*20 + [7]*18 + [8]*8 + [1]*10,
    [2]* 12 + [3]*5 + [4]*8 + [5]*12 + [6]*20 + [7]*18 + [8]*8 + [1]*4,
    [2]* 8 + [3]*8 + [4]*8 + [5]*12 + [6]*20 + [7]*38 + [8]*28 + [1]*11,
    [2]* 23 + [3]*5 + [4]*8 + [5]*12 + [6]*20 + [7]*18 + [8]*8 + [1]*40,
    [2]* 18 + [3]*15 + [4]*28 + [5]*12 + [6]*50 + [7]*18 + [8]*8 + [1]*20,
    [2]* 28 + [3]*25 + [4]*8 + [5]*12 + [6]*20 + [7]*18 + [8]*8 + [1]*10,
    [2]* 28 + [3]*5 + [4]*28 + [5]*12 + [6]*20 + [7]*13 + [8]*7 + [1]*14,
    [2]* 38 + [3]*45 + [4]*8 + [5]*32 + [6]*20 + [7]*18 + [8]*8 + [1]*1,
    [2]* 8 + [3]*5 + [4]*8 + [5]*12 + [6]*20 + [7]*15 + [8]*4 + [1]*6,
]

r.learn("NES", *training_set)



r.dump()

r2 = Recognizer(dumpfile)
r2.load()

print r2.recognize([2]* 16 + [3]*12 + [4]*20 + [5]*15 + [6]*10 + [7]*23 + [8]*13 + [1]*21)


