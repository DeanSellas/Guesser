'''
This class encodes text fed into it to be later used in the scoring algorithm.

It picks random words inside the text and replaces with ${word} this will indicate to the scorer to score this word.

TODO figure out best way to handle text 
'''
import random, time


class Encoder():

    def __init__(self, seed=0):
        self.rand = random
        if(seed < 1):
            seed = int(time.time())
        
        self.rand.seed(seed)
        
        # calculates probability
        self.prob = self.rand.random() * 0.25

    def encode(self, text):
        encodedText = ""
        feedLst = []
        feed = ""
        for word in text.split():
            if self.rand.random() < self.prob:
                # skip any non letter characters
                if not ('a' <= word.lower() <= 'z'):
                    continue
                feedLst.append([feed, word])
                word = "${"+self._clean(word)+"}"
                feed = ""

            else:
                feed += "{} ".format(word)
            encodedText += "{} ".format(word)
        
        return (feedLst, encodedText)

    def decode(self):
        pass

    def _clean(self, word):
        out = ""
        for c in word:
            if 'a' <= c.lower() <= 'z':
                out += c
        return out
