import torch

from src.score import Score
from src.encoder import Encoder

from vendor.lmexplorer.lm_explorer.lm.gpt2 import GPT2LanguageModel

from vendor.logger.logger import Logger

class Guesser():
    def __init__(self, model="gpt2", interact=False, score=False, topK=10, seed=0, Log=None):
        self.model = model
        self.topK = topK
        self.interact = interact
        self._build(seed, Log)
    
    def _build(self, seed, Log):
        if Log == None:
            Log = Logger()

        self.Log = Log
        self.Scorer = Score()
        self.Encoder = Encoder(seed)
        self.GPT = GPT2LanguageModel(model_name=self.model)

    def _run(self, text):
        logits = self.GPT.predict(text, "")
        probabilities = torch.nn.functional.softmax(logits)

        best_indices = logits.topk(self.topK)[1]
        self.best_words = [self.GPT[idx.item()] for idx in best_indices]
        self.best_probabilities = probabilities[best_indices].tolist()
    
    def _getWords(self):
        '''
            returns Top-K Words from GPT-2
        '''
        return self.best_words
    
    def _getPropability(self):
        ''' returns top-k Propabilities from GPT-2 '''
        return [round(p * 100, 2) for p in self.best_probabilities]

    def _process(self, text, guess):
            ''' scores inputted text and logs it '''
            self._run(text)
            outputLst = self._output()
            self.Log.Info(("Answer List : {}".format(outputLst)))

            score = self.Scorer.score(outputLst, guess)
            self.Log.Info(score)
    
    def start(self, text=""):
        ''' 
        starts program

        text = Text to be inputted
        '''

        if text == "" and not self.interact:
            raise EnvironmentError("Please input valid text or use the --interact flag")

        if text != "":
            test = self.Encoder.encode(text=text)
            for item in test[0]:
                if item[0] == '':
                    continue
                self._process(item[0], item[1])

        else:
            while self.interact:
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
                self._process(text, guess)
        
        score = self.Scorer.calcScore()
        self.Log.Info("Score: {}".format(score))
        return score

    def _output(self):
        ''' returns top-k words and propabilities '''
        return [(self._getWords()[i], self._getPropability()[i]) for i in range(self.topK)]
