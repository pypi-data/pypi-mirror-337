import time
import threading

class Timer():
    def __init__(self, timeBetweenCalls=0):
        self.lastCalled = time.time()
        self.queueDict = {}
        self.timeBetweenCalls = timeBetweenCalls
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.running = True

    def add(self, key, function, args=()):
        init = True if self.queueDict == {} else False

        self.queueDict[key] = (function, args)

        if init:
            self.running = True
            self.thread.start()

    def remove(self, key):
        del self.queueDict[key]

        if self.queueDict == {}:
            self.running = False
            self.thread.join()

    def queue(self):
        while self.lastCalled + self.timeBetweenCalls <= time.time():
            self.lastCalled += self.timeBetweenCalls
            self.executeQueue()

    def executeQueue(self):
        for value in self.queueDict.values():
            value[0](*value[1])

    def run(self):
        while self.running:
            self.queue()
            time.sleep(self.timeBetweenCalls)  # Avoids excessive CPU usage

    def stop(self):
        self.running = False
        self.thread.join()

class SecondsQueue(Timer):
    def __init__(self):
        super().__init__(1)

class MinutesQueue(Timer):
    def __init__(self):
        super().__init__(60)

class HoursQueue(Timer):
    def __init__(self):
        super().__init__(3600)

class DaysQueue(Timer):
    def __init__(self):
        super().__init__(86400)

class TickQueue(Timer):
    def __init__(self, speed=60):
        super().__init__(1/speed)

class CustomQueue(Timer):
    def __init__(self, seconds=1):
        super().__init__(seconds)

