from vendor.logger.logger import Logger

class Score():
    '''
        Scorer class takes an input and scores its readability based on the GPT-2 Model Selected
    '''
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
                s = round((item[1] / outList[0][1]) * 100, 2)
                break
        
        out = (text, s)
        self.Log.Info("Score of \'{}\': {}".format(out[0], out[1]))
        
        self.scoreList.append(out)
        return out
    
    def calcScore(self):
        if len(self.scoreList) < 1:
            return 0.0
            
        s = 0
        for item in self.scoreList:
            s += item[1]
        return round(s / (len(self.scoreList) * 100) * 100, 2)

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
