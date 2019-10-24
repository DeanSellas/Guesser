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
        
        s = 0.0
        for item in outList:
            if text == self._remSpecial(item[0]):
                s = (item[1] / outList[0][1]) * 100
                break
        
        out = (text, s)
        self.Log.Info("Score of \'{}\': {}".format(out[0], out[1]))
        
        self.scoreList.append(out)
        return out
    
    def calcScore(self):
        s = 0
        for item in self.scoreList:
            s += item[1]
        return s / (len(self.scoreList) * 100) * 100

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
