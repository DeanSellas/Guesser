'''
This class encodes text fed into it to be later used in the scoring algorithm.

It picks random words inside the text and replaces with ${word} this will indicate to the scorer to score this word.

TODO figure out best way to handle text 
'''
import random


class Encoder():

    def __init__(self, seed=0, maxEncode=25):
        self.rand = random
        
        self.rand.seed(seed)
        
        # probabilty is a random percent based off of maxEncode * random (random is a number between 0 and 1)
        self.prob = self.rand.random() * (maxEncode / 100)
        # print("{0}%".format(round(self.prob*100, 2)))

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
                # tags the word for GPT to guess later
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
