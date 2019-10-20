from vendor.logger.logger import Logger

class Score():
    def __init__(self, mod=0.5, Log=None):
        if Log == None:
            Log = Logger()
        
        self.Log = Log

        self._setMod(mod)

    def score(self, outList, text):
        '''
            Scores guesses with inputed text
        '''
        prob = 0.0
        for item in outList:
            if text == self._remSpecial():
                prob = scoreModifier(item[1])
                break
        self.Log.Info("Score of {}: {}".format(text, prob))
        return (text, prob)
    
    def scoreModifier(self, score):
        return score * self.mod

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
