import os

from fire import Fire

from src.guesser import Guesser

from vendor.logger.logger import Logger
""" OLD SETUP CODE
    model_117M = GPT2LanguageModel(model_name="gpt2")
    logits = model_117M.predict("Joel is", "")
    probabilities = torch.nn.functional.softmax(logits)

    topk = 10

    best_logits, best_indices = logits.topk(topk)
    best_words = [model_117M[idx.item()] for idx in best_indices]
    best_probabilities = probabilities[best_indices].tolist()
    print(best_words)
"""

Log = Logger()
def start(model="gpt2", interact=False, score=False, topK=10, text=""):
    checks(model, topK)
    # MOVE TO LOGGER CLASS
    # 
    Log.Warn(text="Model: {} | Interact: {} | TopK: {} | Text: {}".format(
        model, interact, topK, text))
    guess = Guesser(model, interact, score, topK, Log)
    guess.start()

def checks(model, topK):
    mList = ["gpt2", "gpt2-medium", "gpt2-large"]
    if model not in mList:
        Log.Error("Model Must be a value in {}".format(mList), ValueError)

    if topK < 1:
        Log.Error("TopK must be a value greater than 0", ValueError)

if __name__ == "__main__":
    Fire(start)
