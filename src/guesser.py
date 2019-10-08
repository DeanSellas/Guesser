import torch

from vendor.lmexplorer.lm_explorer.lm.gpt2 import GPT2LanguageModel

class Guesser():
    def __init__(self, model="gpt2", interact=False, topK=10, text=""):
        self.model = model
        self.topK = topK

        if text == "" and not interact:
            raise EnvironmentError("Please input valid text or use the --interact flag")

        self._build()
        self.start(interact, text)
    
    def _build(self):
        self.GPT = GPT2LanguageModel(model_name=self.model)
        return True

    def _run(self, text):
        logits = self.GPT.predict(text, "")
        probabilities = torch.nn.functional.softmax(logits)

        best_logits, best_indices = logits.topk(self.topK)
        self.best_words = [self.GPT[idx.item()] for idx in best_indices]
        self.best_probabilities = probabilities[best_indices].tolist()
    
    def _getWords(self):
        return self.best_words
    
    def _getPropability(self):
        return [round(p * 100, 2) for p in self.best_probabilities]

    def start(self, interact=False, text=""):          
        if text != "":
            self._run(text)
            print(self._output())
            return
        while interact:
                text = input("Input Text >> ")
                self._run(text)
                print(self._output())

    def _output(self):
        words = self._getWords()
        prob = self._getPropability()
        return [(words[i], prob[i]) for i in range(self.topK)]
