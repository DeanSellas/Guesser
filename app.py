import os

from fire import Fire

from src.guesser import Guesser

from vendor.logger.logger import Logger
"""
model_117M = GPT2LanguageModel(model_name="gpt2")
logits = model_117M.predict("Joel is", "")
probabilities = torch.nn.functional.softmax(logits)

topk = 10

best_logits, best_indices = logits.topk(topk)
best_words = [model_117M[idx.item()] for idx in best_indices]
best_probabilities = probabilities[best_indices].tolist()
print(best_words)
"""
log = Logger()
def start(model="gpt2", interact=False, topK=10, text=""):

    # MOVE TO LOGGER CLASS
    # clear = lambda: os.system('cls')
    log.Warn(text="Model: {} | Interact: {} | TopK: {} | Text: {}".format(
        model, interact, topK, text))
    guess = Guesser(model, interact, topK)
    guess.start()

if __name__ == "__main__":
    Fire(start)
