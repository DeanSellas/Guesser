import os

from fire import Fire

from src.guesser import Guesser

from vendor.logger.logger import Logger

from tests import encodeTests

def start(model="gpt2", interact=False, score=False, topK=10, text="", logpath="", tests=False):
    if tests:
        runTests()
        return

    Log = Logger(filePath=logpath)
    checks(model, topK, Log)
    
    Log.Warn(text="Model: {} | Interact: {} | TopK: {} | Text: {}".format(
        model, interact, topK, text))
    guess = Guesser(model, interact, score, topK, Log)
    guess.start()

def checks(model, topK, Log):
    model_List = ["gpt2", "gpt2-medium", "gpt2-large"]
    if model not in model_List:
        Log.Error("Model Must be a value in {}".format(model_List), ValueError)

    if topK < 1:
        Log.Error("TopK must be a value greater than 0", ValueError)

def runTests():
    encodeTests.run()
    

if __name__ == "__main__":
    Fire(start)