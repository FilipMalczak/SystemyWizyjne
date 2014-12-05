from collections import namedtuple
import numpy
import pickle
from hmmlearn import hmm

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
        self._symbols = symbols # todo: reverse this into dict
        self._models = {}
        self._sizes = {}
        self._empty = symbols[0] if symbols else 0
        if symbols is None:
            self.load()

    def load(self):
        with open(self.dump_path, "r") as f:
            (self._symbols, self._models, self._sizes, self._empty) = pickle.load(f)

    def dump(self):
        with open(self.dump_path, "w") as f:
            pickle.dump((self._symbols, self._models, self._sizes, self._empty), f)

    def _hmm_states_number(self):
        # experiment here a little
        return len(self._symbols)

    def _cast_to_ints(self, symbol_vector):
        return [ self._symbols.index(it) for it in symbol_vector ]

    def _fix_length(self, observations, new_len):
        out = observations[:new_len]
        if len(out)<new_len:
            out.extend([self._symbols[0]]*(new_len-len(out)))
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


    def recognize(self, observations, method="viterbi"):
        # todo: figure out, if we want to be able to return None
        return max(self._models.keys(), key=lambda name: self._prob_of_match(observations, name, method))