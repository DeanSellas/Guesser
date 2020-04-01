import os

from fire import Fire

from src.pyReadability import pyReadability
from src.timer import Timer

from vendor.logger.logger import Logger

Log = Logger()
def start(
    model="gpt2",
    interact=False,
    topK=10,
    feed="",
    seed=0,
    mod=1,
    logPath="Log",
    enableTimer=True,
    enableTests=False,
    runs=1,
    probablity=20,
):

    Log.setPath(logPath)

    feedPath = os.path.join("feed", "{}.txt".format(feed))
    checks(model, topK, runs, feedPath, probablity)
    
    if enableTests:
        runTests()
        return
    
    if feedPath != "":
        inFile = open(feedPath, "r", encoding="utf8")
        text = inFile.read()
        inFile.close()

    totalRunTime = None
    if enableTimer:
        t1 = Timer(enableTimer, Log)
        totalRunTime = 0
    Log.setLevel(2)
    out = list()
    for i in range(0, runs):
        Log.Info("STARTING RUN {}".format(i+1))

        Log.Trace(text="Model: {} | Interact: {} | TopK: {} | Text Path: {} | Log Path: {} | Enable Timer: {} | Run Tests: {}".format(model, interact, topK, feed, logPath, enableTimer, enableTests))

        pyRead = pyReadability(model, interact, topK, seed, mod, probablity, Log)

        if enableTimer:
            t1.start()
        # starts pyRead to score the inputted text. If text == null enable interactive mode
        pyRead.start(text)

        runTime = -1
        if enableTimer:
            t1.end()
            runTime = t1.result()
            totalRunTime += runTime
            Log.Info("Took {} Seconds to Score".format(runTime))

        seed = pyRead.getSeed()
        totalWords, wordsEncoded = pyRead.getEncoder().wordsEncoded()
        percentEncoded = round(wordsEncoded/totalWords*100, 2)
        score = pyRead.getScore()

        out.append([seed, totalWords, wordsEncoded, percentEncoded, score, runTime])

        Log.Info("Words Encoded: {} | Total Words: {} | With a score of {}%".format(wordsEncoded, totalWords, score))

    Log.Info("Took {} Seconds to Run {} tests".format(totalRunTime, runs))

    fields = ['seed', 'total words', 'words encoded', 'percent encoded', 'score', 'time']
    Log.csvWriter(feed, fields, out)

def checks(model, topK, runs, feed, probablity):

    model_List = ["gpt2", "gpt2-medium", "gpt2-large"]

    if model not in model_List:
        Log.Error("Model Must be a value in {}".format(model_List), ValueError)

    if topK < 1:
        Log.Error("TopK must be a value greater than 0", ValueError)

    if runs < 1:
        Log.Error("Runs must be a value greater than 0", ValueError)

    if feed != "" and not os.path.exists(feed):
        Log.Error("Feed must be a feed provided in the documentation", ValueError)

    if probablity < 1 or probablity > 75:
        Log.Error("Probablity must be a value greater than 0 and less than 75", ValueError)

def runTests():
    import tests
    tests.encodeTests.run(Log)
if __name__ == "__main__":
    Fire(start)