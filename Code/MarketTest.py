from multiprocessing import Queue, Process, Value
import threading
import time


def handler(Q):
    TransOfDay.append(Q)


def listener(WeatherTab):
    print("Starting Thread :", threading.current_thread().name)
    Q = TransactionsMarket.get()
    gestion = threading.Thread(target=handler, args=(Q))


class worker(Process):
    def __init__(self, name, drapeau):
        super().__init__()
        self.name = name
        self.Flag = drapeau

    def run(self):
        print("starting thread :", self.name)

        while True:
            if self.Flag.value == 1:
                time.sleep(1)
                print(self.name, "a fini de travailler")
        print("Ending thread :", self.name)

if __name__ == "__main__":

    print("starting thread :", threading.current_thread().name)
    TransactionsMarket = Queue()
    thread = threading.Thread(target=listener, args=())
    TransOfDay = list()

    Flag = Value('i', 0)

    trav1 = worker("trav1", Flag)
    trav2 = worker("trav2", Flag)

    trav1.start()
    trav2.start()

    for i in range(0,5):
        print("Début du jour", i, "------------------------")
        Flag.value = 1
        time.sleep(0.1) # Pendant ce temps on veut être sûrs que tous les threads sont lancés (mais n'ont pas encore fini !)
        Flag.value = 0
        time.sleep(3)   # Pendant ce temps on veut être sûrs que tons les threads ont fini.
        #Calcul du nouveau prix

    print("Ending thread :", threading.current_thread().name)