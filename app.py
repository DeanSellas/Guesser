import os

from fire import Fire

from src.pyReadability import pyReadability
from src.timer import Timer

from vendor.logger.logger import Logger

Log = Logger()
out = []
def start(model="gpt2", interact=False, score=False, topK=10, text="", feed="", seed=0, mod=1, logPath="Log\\", enableTimer=False, enableTests=False, runs=1):
    Log.setPath(logPath)
    checks(model=model, topK=topK, runs=runs, Log=Log)
    
    if enableTests:
        runTests()
        return
    
    if feed != "":
        inFile = open(feed, 'r', encoding="utf8")
        text = inFile.read()
        inFile.close()

    if enableTimer:
        t1 = Timer(enableTimer, Log)
    
    for i in range(0, runs):

        Log.Info("STARTING RUN {}".format(i+1))

        Log.Info(text="Model: {} | Interact: {} | TopK: {} | Text Path: {} | Log Path: {} | Enable Timer: {} | Run Tests: {}".format(
            model, interact, topK, feed, logPath, enableTimer, enableTests))
        pyRead = pyReadability(model=model, interact=interact, score=score, topK=topK, seed=seed, mod=mod, Log=Log)

        if enableTimer:
            t1.start()
        
        pyRead.start(text)

        

        runTime = -1
        if enableTimer:
            t1.end()
            runTime = t1.result()
            Log.Info("Took {} Seconds to Score".format(runTime))

        seed = pyRead.getSeed()
        wordedEncoded, totalWords = pyRead.getEncoder().wordsEncoded()
        score = pyRead.getScore()

        out.append([seed, totalWords, wordedEncoded, score, runTime])

        Log.Info("Words Encoded: {} | Total Words: {} | {}%".format(wordedEncoded, totalWords, round(wordedEncoded/totalWords*100, 2)))

    # TODO export this to logging class
    fields = ['seed', 'total words', 'words encoded', 'score', 'time']
    Log.csvWriter(fields, out)

def checks(model, topK, runs, Log):
    model_List = ["gpt2", "gpt2-medium", "gpt2-large"]
    if model not in model_List:
        Log.Error("Model Must be a value in {}".format(model_List), ValueError)

    if topK < 1:
        Log.Error("TopK must be a value greater than 0", ValueError)

    if runs < 1:
        Log.Error("Runs must be a value greater than 0", ValueError)

def runTests():
    import tests
    tests.encodeTests.run(Log)
    

if __name__ == "__main__":
    Fire(start)