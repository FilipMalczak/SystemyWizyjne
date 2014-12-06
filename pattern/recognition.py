import numpy
import os
import pickle
from hmmlearn import hmm

# SYMBOLS = "X N NE E SE S SW W NW"
SYMBOLS = range(9)
DUMP_PATH = os.path.join(os.path.dirname(__file__), "default.recognizer")

def default_recognizer():
    out = Recognizer(DUMP_PATH, SYMBOLS)
    if os.path.exists(DUMP_PATH):
        out.load()
    return out


def _median(l, key=lambda x: x):
    if (len(l)<2):
        return l[0]
    return key(sorted(l, key=key)[int(len(l)/2)])

class Recognizer:
    def __init__(self, dump_path, symbols=None):
        '''
        :param dump_path Path to file in which Recognizer will be stored
        :param symbols: List of observable symbols. All observations used in public methods must consist of
                        these elements. First element of list will be used as empty symbol. Empty symbol
                        should not occur in observations, but only be added internally by recognizer.
        '''
        self.dump_path = dump_path
        if symbols is None:
            self.load()
        else:
            self._symbols_idxs = self._reverse_indexing(symbols)
        self._models = {}
        self._sizes = {}
        self._empty = symbols[0] if symbols else 0


    def _reverse_indexing(self, l):
        return { l[i]: i for i in xrange(len(l)) }

    def load(self):
        with open(self.dump_path, "r") as f:
            (self._symbols_idxs, self._models, self._sizes, self._empty) = pickle.load(f)

    def dump(self):
        with open(self.dump_path, "w") as f:
            pickle.dump((self._symbols_idxs, self._models, self._sizes, self._empty), f)

    def _hmm_states_number(self):
        #todo: experiment here a little
        return len(self._symbols_idxs)

    def _cast_to_ints(self, symbol_vector):
        return [ self._symbols_idxs[it] for it in symbol_vector ]

    def _fix_length(self, observations, new_len):
        out = observations[:new_len]
        if len(out)<new_len:
            out.extend([self._empty]*(new_len-len(out)))
        return out

    def learn(self, pattern_name, *observations_lists):
        '''
        Thanks to *args we can learn by one, or by many examples with the same method.
        '''
        new_len = self._sizes.setdefault(pattern_name, _median(observations_lists, len))
        model = self._models.setdefault(pattern_name, hmm.GaussianHMM(self._hmm_states_number()))
        training_matrix = []
        for it in observations_lists:
            training_matrix.append(self._cast_to_ints(
                self._fix_length(it, new_len)
            ))
        training_matrix = numpy.array(training_matrix, numpy.int_)
        model.fit([training_matrix])

    def _prob_of_match(self, observations, pattern_name, method):
        new_len = self._sizes[pattern_name]
        obs = numpy.array([self._cast_to_ints(self._fix_length(observations, new_len))], numpy.int_)
        return self._models[pattern_name].decode(obs, method)[0]

    def is_pattern_known(self, pattern_name):
        return pattern_name in self._models.keys()



    def recognize(self, observations, method="viterbi"):
        #todo: allow returning None
        return max(self._models.keys(), key=lambda name: self._prob_of_match(observations, name, method))