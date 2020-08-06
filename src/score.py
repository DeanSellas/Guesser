from vendor.logger.logger import Logger

class Score():
    '''
        Scorer class takes an input and scores its readability based on the GPT-2 Model Selected
    '''
    def __init__(self, mod=1, Log=None):
        if Log == None:
            Log = Logger()
        
        self._totalNormScore = 0
        self._totalUnnormScore = 0

        self.Log = Log
        self.scoreList = list()
        self._setMod(mod)

    # MAIN FUNCTION USED FOR SCORING
    def score(self, guessList, text):
        '''
            Scores guesses with inputed text

            guesslist: is a list of strings and probabilities for potential next words

            text is the actual next word in the string
        '''
        
        total = 0
                
        for s in guessList:
            total += s[1]

        # Score is the return value - init it 0
        norm_score = 0.0

        unnorm_score = 0.0

        # loop through items in the guess list taken from gpt
        # guess will be a tuple (WORD, PERCENT CHANCE)        
        for guess in guessList:

            # if actual word matches the guess word, score the word
            if text == self._remSpecial(guess[0]):

                # Score is equal to CHANCE_OF_WORD / totalprob * 100
                norm_score = guess[1] / total * 100

                unnorm_score = guess[1]

                # round score to nearest 0.xx
                norm_score = round(norm_score, 2)
                # if score is greater than 100 (due to modifier) set it to be 100
                if norm_score > 100:
                    norm_score = 100
                break
        self._totalNormScore += norm_score
        self._totalUnnormScore += unnorm_score
        
        # stores text and score in a tuple and appends it the scorelist before returning it
        output = (text, norm_score, unnorm_score)
        self.scoreList.append(output)
        return output
    
    def calcScore(self):
        ''' Calculates total score '''
        if len(self.scoreList) < 1:
            return 0.0


        # move 100s
        # rounds adverage score to the nearest x.xx place
        return (round(self._totalNormScore / (len(self.scoreList) * 100) * 100, 2), self._totalUnnormScore)

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