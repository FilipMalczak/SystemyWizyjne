from collections import defaultdict
import numpy
import os
import pickle
from hmmlearn import hmm
import sys
from pattern.decision import default_decider

print sys.path
from common import dirs
from common.config import obs_length, states

SYMBOLS = range(9)

def default_recognizer():
    out = Recognizer(default_decider(), SYMBOLS)
    out.load()
    return out


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

    def __init__(self, decider, symbols=None, length=obs_length, states=states):
        '''
        :param decider: instance of pattern.decision.Decider
        :param symbols: List of observable symbols. All observations used in public methods must consist of
                        these elements. First element of list will be used as empty symbol. Empty symbol
                        should not occur in observations, but only be added internally by recognizer.
        :param length: integer stating how long should observations be. If they are too long, they are cut
                        down, if they are too short, some empty symbols are appended
        :param states: number of HMM states
        '''
        self._decider = decider
        if symbols is None:
            self.load()
        else:
            self._symbols_idxs = self._reverse_indexing(symbols)
        self._models = {}
        self._training_obs = defaultdict(list)
        self._obs_length = length
        self._states = states
        self._empty = symbols[0] if symbols else 0
        self._active = []
        self._dirty = False
        self._recalculate()

    def _recalculate(self):
        self._dirty = self._decider.recalculate(self._training_obs, lambda name, obs: self._prob_of_match(obs, name, "viterbi"))

    def _reverse_indexing(self, l):
        return { l[i]: i for i in xrange(len(l)) }

    def load(self):
        if os.path.exists(dirs.hmm_state):
            with open(dirs.hmm_state, "r") as f:
                (
                    self._symbols_idxs,
                    self._active,
                    self._obs_length,
                    self._state
                ) = pickle.load(f)
            # with open(dirs.prob_boundaries, "r") as f:
            #     self._bounds = pickle.load(f)
            for pattern in self._active:
                with open(dirs.model(pattern), "r") as f:
                    (self._models[pattern], self._training_obs[pattern]) = pickle.load(f)
        self._dirty = False
        self._recalculate()

    def dump(self):
        with open(dirs.hmm_state, "w") as f:
            pickle.dump(
                (
                    self._symbols_idxs,
                    self._active,
                    self._obs_length,
                    self._states
                ),
                f
            )
        # with open(dirs.prob_boundaries, "w") as f:
        #     pickle.dump(self._bounds, f)
        for pattern in self._active:
            with open(dirs.model(pattern), "w") as f:
                pickle.dump((self._models[pattern], self._training_obs[pattern]), f)

    def activate(self, name):
        if not name in self._active:
            if os.path.exists(dirs.model(name)):
                with open(dirs.model(name), "r") as f:
                    (self._models[name], self._training_obs[name]) = pickle.load(f)
                self._dirty = True
            else:
                raise Exception("Pattern "+name+" doesn't exist, so it cannot be activated!")
        self.dump()

    def deactivate(self, name):
        assert name in self._active, "Pattern "+name+" isn't active, so it cannot be deactivated!"
        self._active.remove(name)
        with open(dirs.model(name), "w") as f:
            pickle.dump((self._models[name], self._training_obs[name]), f)
        del self._models[name]
        del self._training_obs[name]
        self._dirty = True
        self.dump()

    def remove(self, name):
        '''
        Ensures that there is no trace of such pattern - whether it was active, inactive or didn't exist,
        outcome is the same.
        '''
        if name in self._active:
            self._active.remove(name)
            self._dirty = True
        if os.path.exists(dirs.model(name)):
            os.remove(dirs.model(name))
        if name in self._models:
            del self._models[name]
        if name in self._training_obs:
            del self._training_obs[name]
        self.dump()


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
        out = self._models[pattern_name].decode(obs, method)[0]
        print pattern_name, out
        return out

    def is_pattern_known(self, pattern_name):
        return pattern_name in self._models.keys()


    def recognize(self, observations, method="viterbi"):
        '''
        :return: tuple (most_probable_pattern_name, ranking) where ranking is list of tuples (pattern name, log of prob, boundary)
                containing only those patterns that have results above boundary
        '''
        print self._active
        if self._dirty:
            self._recalculate()
            # self._dirty = False
        probs = {}
        for pattern in self._active:
            probs[pattern] = self._prob_of_match(observations, pattern, method)
        out = self._decider.decide(probs)
        return out[0] if len(out) else None, out