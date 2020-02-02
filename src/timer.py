import time

class Timer():

    def __init__(self, enable, Log):
        self._enable = enable
        self._startTime = 0
        self._endTime = -1
        self._dif = -1
        self.Log = Log

    def start(self):
        self._startTime = time.time()
    
    def end(self):
        self._endTime = time.time()
        self._dif = self._endTime - self._startTime

    def result(self, n=2):
        return round(self._dif, n)
        
    def reset(self):
        self._startTime = 0
        self._endTime = -1
        self._dif = -1