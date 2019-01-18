from multiprocessing import Process
import signal
import os
import random
import time


class External(Process):
    def __init__(self):
        super().__init__()


    def run(self):
        while True:
            time.sleep(random.randint(1, 2))
            print("Choix du signal")
            cata = random.randint(1, 2)
            if cata == 1:
                os.kill(os.getppid(), signal.SIGUSR1) # 1 = Trouble social  (3 = pénurie matière première)
            elif cata == 2:
                os.kill(os.getppid(), signal.SIGUSR2) # 2 = Tension Diplomatique



if __name__ == "__main__":

    ExternalValues = [0, 0]

    def handler(sig, frame):
        if sig == signal.SIGUSR1:
            print("Catastrophe ! Trouble social")
            ExternalValues[0] = 1
            ExternalValues[1] = 1.5
            print(ExternalValues)

        elif sig == signal.SIGUSR2:
            print("Catastrophe ! Tension diplomatique")
            ExternalValues[0] = 1
            ExternalValues[1] = 2
            print(ExternalValues)

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    p = External()

    Prix = 100
    p.start()

    time.sleep(5)
    print("Prix = ", Prix * ExternalValues[1])

    p.join()