from vendor.logger.logger import Logger

class Score():
    '''
        Scorer class takes an input and scores its readability based on the GPT-2 Model Selected
    '''
    def __init__(self, mod=1, Log=None):
        if Log == None:
            Log = Logger()
        
        self._totalScore = 0

        self.Log = Log
        self.scoreList = list()
        self._setMod(mod)

    def score(self, guessList, text):
        '''
            Scores guesses with inputed text

            guesslist is a list of strings and probabilities for potential next words

            text is the actual next word in the string
        '''
        
        # 
        score = 0.0
        for item in guessList:
            if text == self._remSpecial(item[0]):
                score = item[1] / guessList[0][1] * 100 + self.Mod
                score = round(score, 2)
                if score > 100:
                    score = 100
                break
        self._totalScore += score
        
        # stores text and score in a tuple and appends it the scorelist before returning it
        output = (text, score)
        self.scoreList.append(output)
        return output
    
    def calcScore(self):
        ''' Calculates total score '''
        if len(self.scoreList) < 1:
            return 0.0

        # rounds adverage score to the nearest x.xx place
        return round(self._totalScore / (len(self.scoreList) * 100) * 100, 2)

    def _setMod(self, mod):
        ''' Sets modifier variable '''
        self.Mod = mod
    
    def _remSpecial(self, text=""):
        '''
            Removes Special Characters from a string of text
        '''
        remSpec = ""
        for s in text.lower():
            if 'a' <= s <= 'z':
                remSpec += s
        return remSpec
