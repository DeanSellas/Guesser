import torch, time

from src.score import Score
from src.encoder import Encoder

from vendor.lmexplorer.lm_explorer.lm.gpt2 import GPT2LanguageModel

from vendor.logger.logger import Logger

import random

class pyReadability():
    '''
        Main class for the applicaiton. Loads the data, encodes it and runs scoring algortim.
    '''
    def __init__(self, model, interact, topK, seed, mod, probabilty, Log=None):
        self.model = model
        self.topK = topK
        self.interact = interact
        self._seed = seed
        self._probabilty = probabilty
        self._score = -1
        

        self._build(mod, Log)
    
    def _build(self, mod, Log):
        if Log == None:
            Log = Log()

        if(self._seed < 1):
            random.seed(time.time())
            self._seed = random.random()

        self.Log = Log
        self.Scorer = Score(mod, self.Log)
        self.Encoder = Encoder(seed=self._seed, probabilty=self._probabilty)
        self.GPT = GPT2LanguageModel(model_name=self.model)

    def _run(self, text):
        logits = self.GPT.predict(text, "")
        probabilities = torch.nn.functional.softmax(logits)

        best_indices = logits.topk(self.topK)[1]
        self.best_words = [self.GPT[idx.item()] for idx in best_indices]
        self.best_probabilities = probabilities[best_indices].tolist()
    
    def _getWords(self):
        ''' returns Top-K Words from GPT-2 '''
        return self.best_words
    
    def _getPropability(self):
        ''' returns top-k Propabilities from GPT-2 '''
        return [round(p * 100, 2) for p in self.best_probabilities]

    def _process(self, text, guess):
            ''' scores inputted text and logs it '''
            self._run(text)
            outputLst = self._output()
            self.Log.Trace(("Answer List : {}".format(outputLst)))

            score = self.Scorer.score(outputLst, guess)
            self.Log.Trace(score)

            self.Log.Info("Score of \'{}\': {}".format(score[0], score[1]))
    
    def start(self, text=""):
        ''' 
            starts program

            text = Text to be inputted
        '''

        if text == "" and not self.interact:
            raise EnvironmentError("Please input valid text or use the --interact flag")

        if text != "":
            encoded = self.Encoder.encode(text=text)
            for item in encoded[0]:
                if item[0] == '':
                    continue
                self._process(item[0], item[1])
                
        # Code for Manual Input, meant for debugging not for production use
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
        
        self._score = self.Scorer.calcScore()
        self.Log.Info("Normalized Score: {} | Unnormalized Score: {}".format(self.getNormScore(), self.getUnNormScore()))
        

    def getNormScore(self):
        ''' returns the normalized score '''
        return self._score[0]

    def getUnNormScore(self):
        ''' returns the unormalized score '''
        return self._score[1]

    def getSeed(self):
        ''' returns the seed used '''
        return self._seed

    def getEncoder(self):
        ''' returns the encoder object '''
        return self.Encoder

    def _output(self):
        ''' returns top-k words and propabilities '''
        return [(self._getWords()[i], self._getPropability()[i]) for i in range(self.topK)]
