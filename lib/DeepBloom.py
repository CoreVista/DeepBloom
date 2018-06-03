from BloomFilter import BloomFilter
import math
import random
from utils import *
import mmh3

class DeepBloom(object):
    def __init__(self, model, data, fp_rate):
        self.model = model
        self.threshold = None
        self.fp_rate = float(fp_rate)
        self.fit(data)
        self.create_bloom_filter(data)

    def check(self, item):
        # print(self.model.predict(item))
        if self.model.predict(item) > self.threshold:
            return True
        return self.bloom_filter.check(item)

    def create_bloom_filter(self, data):
        false_negatives = []
        for positive in data.positives:
            if self.model.predict(positive) <= self.threshold:
                false_negatives.append(positive)

        self.bloom_filter = BloomFilter(
            len(false_negatives),
            self.fp_rate / 2,
            string_digest
        )
        for fn in false_negatives:
            self.bloom_filter.add(fn)


    ## For now, only train the first model.
    def fit(self, data):
        ## Split negative data into subgroups.
        (s1, s2) = split_negatives(data)

        ## Shuffle together subset of negatives and positives.
        ## Then, train the model on this data.
        shuffled = shuffle_for_training(s1, data.positives)
        self.model.fit(shuffled[0], shuffled[1])

        ## We want a threshold such that at most s2.size * fp_rate/2 elements
        ## are greater than threshold.
        fp_index = math.ceil((len(s2) * (1 - self.fp_rate/2)))
        predictions = [self.model.predict(item) for item in s2]
        predictions.sort()
        self.threshold = predictions[fp_index]

