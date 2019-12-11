import os

from fire import Fire

from src.pyReadability import pyReadability

from vendor.logger.logger import Logger

Log = Logger()
def start(model="gpt2", interact=False, score=False, topK=10, text="", seed=0, logpath="", tests=False):
    if tests:
        runTests()
        return

    Log.setPath(logpath)
    checks(model, topK, Log)
    
    Log.Info(text="Model: {} | Interact: {} | TopK: {} | Text: {} | Log Path: {} | Tests: {}".format(
        model, interact, topK, text, logpath, tests))
    pyRead = pyReadability(model, interact, score, topK, seed, Log)
    pyRead.start(text)

def checks(model, topK, Log):
    model_List = ["gpt2", "gpt2-medium", "gpt2-large"]
    if model not in model_List:
        Log.Error("Model Must be a value in {}".format(model_List), ValueError)

    if topK < 1:
        Log.Error("TopK must be a value greater than 0", ValueError)

def runTests():
    from tests import encodeTests
    encodeTests.run(Log)
    

if __name__ == "__main__":
    Fire(start)