'''
This class encodes text fed into it to be later used in the scoring algorithm.

It picks random words inside the text and replaces with ${word} this will indicate to the scorer to score this word.

TODO figure out best way to handle text 
'''
import random


class Encoder():

    def __init__(self, seed=0, probabilty=25):
        self.rand = random
        
        self.rand.seed(seed)
        
        self.textLen = 0
        self.encodedWords = 0
        # probabilty is a random percent based off of maxEncode * random (random is a number between 0 and 1)
        # self.probabilty = self.rand.random() * (probabilty/ 100)
        # print("{0}%".format(round(self.probabilty*100, 2)))
        self.probabilty = probabilty / 100

    def encode(self, text):
        
        encodedText = ""
        feedLst = []
        feed = ""
        useNext = False
        self.textLen = len(text.split())
        for word in text.split():
            if useNext or self.rand.random() <= self.probabilty:
                # skip any non letter characters
                if not ('a' <= word.lower() <= 'z'):
                    useNext = True
                    continue
                feedLst.append([feed, word])
                # tags the word for GPT to guess later
                word = "${"+self._clean(word)+"}"
                feed = ""
                self.encodedWords += 1
                useNext = False

            else:
                feed += "{} ".format(word)
            encodedText += "{} ".format(word)

        return (feedLst, encodedText)

    def decode(self):
        pass
    
    def getProbablity(self):
        return self.probabilty

    def wordsEncoded(self):
        return (self.encodedWords, self.textLen)

    def _clean(self, word):
        out = ""
        for c in word:
            if 'a' <= c.lower() <= 'z':
                out += c
        return out
