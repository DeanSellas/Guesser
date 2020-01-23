import torch

from src.score import Score
from src.encoder import Encoder

from vendor.lmexplorer.lm_explorer.lm.gpt2 import GPT2LanguageModel

from vendor.logger.logger import Logger

class Guesser():
    def __init__(self, model="gpt2", interact=False, score=False, topK=10, Log=None, Scorer=None):
        self.model = model
        self.topK = topK
        self._build(Log, Scorer)
    
    def _build(self, Log, Scorer):
        if Log == None:
            Log = Logger()
        if Scorer == None:
            Scorer = Score()

        self.Log = Log
        self.Scorer = Scorer
        self.Encoder = Encoder()
        self.GPT = GPT2LanguageModel(model_name=self.model)

    def _getBestWords(self, text):
        ''' Creates finds best words and calculates their propbablity of occuring ''' 
        logits = self.GPT.predict(text, "")
        
        best_logits, best_indices = logits.topk(self.topK)

        # converts best indicie list into a list of words
        best_words = [self.GPT[idx.item()] for idx in best_indices]
        
        # calculates probabilities
        probabilities = torch.nn.functional.softmax(logits)

        # creates a list of probabilites based on best_indicies. This is a parallel array to best_words
        best_probabilities = self._getPropability(probabilities[best_indices].tolist())

        # returns a list of tuples. each tuple contains the world in position 0 and the probability in position 1
        return [(best_words[i], best_probabilities[i]) for i in range(self.topK)]
    
    def _getPropability(self, probabilities):
        ''' returns top-k Propabilities from GPT-2 '''
        return [round(p * 100, 2) for p in probabilities]

    def _run(self, text, guess):
            ''' scores inputted text and logs it '''

            # gives a list of the best words that GPT predicts
            guessList = self._getBestWords(text)
            self.Log.Info(("Answer List : {}".format(guessList)))

            # scores guess word with the list of preditions
            score = self.Scorer.score(guessList, guess)
            self.Log.Info(score)
    
    def start(self, text=""):
        '''
        Starts The Program

        text: Text to be fed into GPT. If left blank initiate interactive mode
        '''

        if text != "":
            encoded_text = self.Encoder.encode(text=text)
            for text, guess in encoded_text[0]:
                if text == '':
                    continue
                self._run(text, guess)

        else:
            while True:
                text = self.Log.Input("Input Text >> ")

                if text == "":
                    self.Log.Info("Please provide a valid input")
                    continue
                
                if text == "#?":
                    self.Log.Info("Available Commands: \n#?: Shows available commands\n#end: Ends Execution")
                    continue

                if text == "#end":
                    self.Log.Info("Ending Program")
                    break

                guess = self.Log.Input("What will the next word be >> ")
                self._run(text, guess)
            
        self.Log.Info("Score: {}".format(self.Scorer.calcScore()))
