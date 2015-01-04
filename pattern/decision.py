
def mean(l, key=lambda x: x):
    return 1.0*sum(map(key, l))/len(l)

def median(l, key=lambda x: x):
    if (len(l)<2):
        return l[0]
    return key(sorted(l, key=key)[int(len(l)/2)])

def default_decider():
    # return CentroidDecider(mean, False)
    return CentroidDecider(median, False)

class Decider:
    def recalculate(self, training_data, prob):
        '''
        Refresh all internal data according to provided arguments.
        :param training_data: map(pattern_name -> list(list(symbol: int)))
        :param prob: function(pattern_name, list(symbol))->float
        :return: None
        '''

    def decide(self, probs):
        '''
        Decide which pattern is detected.
        :params probs: map(pattern_name -> prob: float)
        :return: list(tuple(detected_pattern, prob)) ordered descending by probability of detection
        '''

class CentroidDecider(Decider):
    def __init__(self, centroid_finder, divide=False):
        '''
        :param centroid_finder: function(list(prob: float))->centroid: float
        :param divide: boolean, if true decision is based on prob / boundary; if false on prob - boundary
        '''
        self.boundaries = {}
        self.centroid_finder = centroid_finder
        self.divide = divide


    def recalculate(self, training_data, prob):
        self.boundaries.clear()
        if len(training_data)>1:
            for current in training_data.keys():
                centroids = {}
                for pattern_name, obs_list in training_data.iteritems():
                    # print pattern_name, len(obs_list), obs_list[0] if len(obs_list) else ""
                    centroids[pattern_name] = self.centroid_finder(map(lambda x: prob(current, x), obs_list))
                keys = training_data.keys()
                keys.remove(current)
                self.boundaries[current] = (centroids[current] + centroids[min(keys, key=lambda x: abs(centroids[x]-centroids[current]))])/2.0
            return True
        return False

    def decide(self, probs):
        out = []
        for k, v in probs.iteritems():
            if v>self.boundaries[k]:
                out.append((k, v))
        op = (lambda k, v : v/self.boundaries[k]) if self.divide else (lambda k, v : v-self.boundaries[k])
        return sorted(out, key=lambda pair: op(*pair), reverse=True)
