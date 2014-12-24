from collections import defaultdict
import numpy
import os
import pickle
from hmmlearn import hmm
import sys
print sys.path
from common import dirs
from common.config import obs_length, states


SYMBOLS = range(9)

def default_recognizer():
    out = Recognizer(SYMBOLS)
    out.load()
    return out


def _median(l, key=lambda x: x):
    if (len(l)<2):
        return l[0]
    return key(sorted(l, key=key)[int(len(l)/2)])

class Recognizer:
    '''
    Recognizer is kept in FS hierarchy:
    - recognition
    -- hmm_state.json - keeps number of states, observation length, and active patterns
    -- probs.json - maps pattern names (also inactive patterns) into boundaries (see below)
    -- models
    --- <pattern_name>.dat - pickled tuples (hmm, training_observations), where hmm is hmmlearn object,
                            and training observations are observations used to teach some symbol (already
                            preprocessed); inactive models are stored here too

    "active" pattern is one that is kept in memory. Only loaded patterns are considered while recognizing.
    We can activate and deactivate patterns with activate/deactivate methods. Recognizer loaded from file will
    have all active patterns that were active while dumping.

    Boundaries are just probability (its log, actually) thresholds, used to decide whether some pattern
    was observed or not.
    See _recalculate method to understand how they are calculated.
    Patterns are ranked by maximizing prob_log/boundary value for each pattern for given observation.
    If prob_log is lower than boundary, pattern is considered not matched and is not used for ranking.

    '''

    def __init__(self, symbols=None, length=obs_length, states=states):
        '''
        :param symbols: List of observable symbols. All observations used in public methods must consist of
                        these elements. First element of list will be used as empty symbol. Empty symbol
                        should not occur in observations, but only be added internally by recognizer.
        :param length: integer stating how long should observations be. If they are too long, they are cut
                        down, if they are too short, some empty symbols are appended
        :param states: number of HMM states
        '''
        if symbols is None:
            self.load()
        else:
            self._symbols_idxs = self._reverse_indexing(symbols)
        self._models = {}
        self._training_obs = defaultdict(list)
        self._obs_length = length
        self._states = states
        self._empty = symbols[0] if symbols else 0
        self._bounds = {}
        self._active = []
        self._dirty = True


    def _reverse_indexing(self, l):
        return { l[i]: i for i in xrange(len(l)) }

    def load(self):
        if os.path.exists(dirs.hmm_state):
            with open(dirs.hmm_state, "r") as f:
                (
                    self._symbols_idxs,
                    self._active,
                    self._obs_length,
                    self._states,
                    self._dirty
                ) = pickle.load(f)
            with open(dirs.prob_boundaries, "r") as f:
                self._bounds = pickle.load(f)
            for pattern in self._active:
                with open(dirs.model(pattern), "r") as f:
                    (self._models[pattern], self._training_obs[pattern]) = pickle.load(f)

    def dump(self):
        with open(dirs.hmm_state, "w") as f:
            pickle.dump(
                (
                    self._symbols_idxs,
                    self._active,
                    self._obs_length,
                    self._states,
                    self._dirty
                ),
                f
            )
        with open(dirs.prob_boundaries, "w") as f:
            pickle.dump(self._bounds, f)
        for pattern in self._active:
            with open(dirs.model(pattern), "w") as f:
                pickle.dump((self._models[pattern], self._training_obs[pattern]), f)

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
        self._dirty = True
        if not pattern_name in self._active:
            self._models[pattern_name] = hmm.GaussianHMM(self._states)
            self._active.append(pattern_name)
        model = self._models[pattern_name]
        training_matrix = []
        for it in observations_lists:
            training_matrix.append(self._cast_to_ints(
                self._fix_length(it, self._obs_length)
            ))
        self._training_obs[pattern_name].extend(training_matrix)
        training_matrix = numpy.array(training_matrix, numpy.int_)
        model.fit([training_matrix])

    def _prob_of_match(self, observations, pattern_name, method):
        new_len = self._obs_length
        obs = numpy.array([self._cast_to_ints(self._fix_length(observations, new_len))], numpy.int_)
        return self._models[pattern_name].decode(obs, method)[0]

    def is_pattern_known(self, pattern_name):
        return pattern_name in self._models.keys()

    def recalculate_boundaries(self):
        '''
        Recalculates only active
        '''
        for key in self._active:
            self._bounds[key] = self._recalculate(key)

    def _recalculate(self, pattern_name, method="viterbi"):
        prob_logs_per_pattern = defaultdict(list)
        for checked in self._active:
            prob_logs_per_pattern[checked] = [
                self._prob_of_match(x, pattern_name, method)
                for x in self._training_obs[checked]
            ]
        # centroid_maker = lambda l : 1.0*sum(l)/len(l)
        centroid_maker = _median
        prob_centroids = {
            k: centroid_maker(v)
            for k,v in prob_logs_per_pattern.iteritems()
        }
        max_diff = 0.0
        out = prob_centroids[pattern_name]
        for k, v in prob_centroids.iteritems():
            diff = v - prob_centroids[pattern_name]
            if diff>max_diff:
                max_diff = diff
                out = v
        return out

    def recognize(self, observations, method="viterbi"):
        '''
        :return: tuple (most_probable_pattern_name, ranking) where ranking is list of tuples (pattern name, log of prob, boundary)
                containing only those patterns that have results above boundary
        '''
        #todo: allow returning None
        if self._dirty:
            self.recalculate_boundaries()
            self._dirty = False
            self.dump()
        out = []
        for pattern in self._active:
            prob_log = self._prob_of_match(observations, pattern, method)
            boundary = self._bounds[pattern]
            if prob_log>boundary:
                out.append((pattern, prob_log, boundary))
        out = sorted(out, key=lambda x: x[1]/x[2], reverse=True)
        return out[0] if len(out) else None, out