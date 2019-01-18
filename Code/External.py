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
                os.kill(os.getpid(), signal.SIGUSR1) # 1 = Trouble social  (3 = pénurie matière première)
            elif cata == 2:
                os.kill(os.getpid(), signal.SIGUSR2) # 2 = Tension Diplomatique



def handler(sig, frame):
    if sig == signal.SIGUSR1:
        print("Catastrophe ! Trouble social")

    elif sig == signal.SIGUSR2:
        print("Catastrophe ! Tension diplomatique")
        Beta = 2


if __name__ == "__main__":
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    p = External()

    Prix = 100
    p.start()

    global externalPID
    externalPID = p.pid
    print(externalPID)

    p.join()