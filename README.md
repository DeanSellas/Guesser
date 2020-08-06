# pyReadability
This python application can take in a series of text and analyze it with GPT-2 and determine its readablity.

# Features

## Flags
```
model - Defines the Text Model to be used by GTP-2. Default Value: "gpt2"
interact - Enables interactive mode. Default Value: False
topK - How many words to test against. Default Value: 10
text - User fed in text. Please Use feed for better results. Default Value: "" 
feed - Prebuilt text to feed into the algorithm. Default Value: ""
seed - Seed used to encode the text. Default Value: 0
mod=1,
logPath - Path to store Logs in. Default Value: "Log"
enableTimer - Enables Timer. Default Value: False
enableTests - Runs Tests, should only be used when developing. Default Value: False
runs - Number of times to run GPT-2 Program. Default Value: 1
probablity - Percentage of words to be encoded and tested in side a text. Default Value: 25
```

### Feed
I have scraped information from the web for testing and proof of concept. To use this data add the `--feed` tag and use one of the names provided below. Ex. `python pyReader ... --feed=netflix`

If you would like to add your own feeds just use the name of the file excluding the extention. Example: Filename: `somefile.txt` Code: `--feed="somefile"`

* netflix

more will be added later.

### Interactive Mode
This mode allows the user to interact with GTP-2 and see outputs in real time. Was originally developed for testing purposes but was left in the codebase if needed in the future. Enable by using the `--interact` flag.
This mode may be buggy and is not fully supported. Use at your own discresion.

# Credits and Aknowlegements
### Contributors
* [Dean Sellas](https://deansellas.com/)

### Repositories
* [Transformers](https://github.com/huggingface/transformers)
* [lm-explorer](https://github.com/allenai/lm-explorer)

This project is a work in progress and is being developed for the research of Professor Mathew Stern of Depaul University