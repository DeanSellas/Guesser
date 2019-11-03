import torch

from src.score import Score

from vendor.lmexplorer.lm_explorer.lm.gpt2 import GPT2LanguageModel

from vendor.logger.logger import Logger

class Guesser():
    def __init__(self, model="gpt2", interact=False, score=False, topK=10, Log=None, Scorer=None):
        self.model = model
        self.topK = topK
        self.interact = interact
        self._build(Log, Scorer)
    
    def _build(self, Log, Scorer):
        if Log == None:
            Log = Logger()
        if Scorer == None:
            Scorer = Score()

        self.Log = Log
        self.Scorer = Scorer
        self.GPT = GPT2LanguageModel(model_name=self.model)

    def _run(self, text):
        logits = self.GPT.predict(text, "")
        probabilities = torch.nn.functional.softmax(logits)

        best_logits, best_indices = logits.topk(self.topK)
        self.best_words = [self.GPT[idx.item()] for idx in best_indices]
        self.best_probabilities = probabilities[best_indices].tolist()
    
    def _getWords(self):
        '''
            returns Top-K Words from GPT-2
        '''
        return self.best_words
    
    def _getPropability(self):
        '''
            returns Top-K Propabilities from GPT-2
        '''
        return [round(p * 100, 2) for p in self.best_probabilities]

    def start(self, text="", nextWord=""):

        def _process(text, guess):
            self._run(text)
            ansList = self._output()
            self.Log.Info(("Answer List : {}".format(ansList)))

            score = self.Scorer.score(ansList, guess)
            self.Log.Info(score)

        if text == "" and not self.interact:
            raise EnvironmentError("Please input valid text or use the --interact flag")

        if text != "":
            _process(text, nextWord)
            return

        while self.interact:
            text = self.Log.Input("Input Text >> ")

            if text == "":
                self.Log.Info("please provide a valid input")
                continue

            if text == "#end":
                self.Log.Info("Ending Program")
                break

            guess = self.Log.Input("What will the next word be >> ")
            _process(text, guess)
            

        self.Log.Info(self.Scorer.calcScore())

    def _output(self):
        return [(self._getWords()[i], self._getPropability()[i]) for i in range(self.topK)]
