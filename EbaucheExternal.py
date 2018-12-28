import random
import time
from multiprocessing import Process
import signal
import os



class ExternalChild(Process):
    def __init__(self):
        super().__init__()
        this.mu = random.randrange(0, 2)   #mu : 0--> Pas d'évenement     1--> Un evenement d'importance Beta
        this.Beta = random.randrange(0, 11)
        this.tabToSend = [this.mu, this.Beta]
    def run(self):
        os.kill(market.pid, this.tabToSend)


if __name__ == "__main__":
    p = ExternalChild()
    p.start()
    p.join()

