from vendor.logger.logger import Logger

class Score():
    def __init__(self, mod=1, Log=None):
        if Log == None:
            Log = Logger()
        
        self.Log = Log
        self.scoreList = list()
        self._setMod(mod)

    def score(self, outList, text):
        '''
            Scores guesses with inputed text
        '''

        def scoreModifier(score):
            return score * self.mod
        
        prob = 0.0
        for item in outList:
            if text == self._remSpecial(item[0]):
                prob = scoreModifier(item[1])
                break
        self.Log.Info("Score of {}: {}".format(text, prob))
        score = (text, prob)
        self.scoreList.append((text, prob))
        return score
    
    def calcScore(self):
        s = 0
        for item in self.scoreList:
            s += item[1]
        return s

    def _setMod(self, mod):
        self.mod = mod
    
    def _remSpecial(self, text=""):
        '''
            Removes Special Characters from a string of text
        '''
        remSpec = ""
        for s in text.lower():
            if 'a' <= s <= 'z':
                remSpec += s
        return remSpec
