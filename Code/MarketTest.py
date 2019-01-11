from multiprocessing import Queue, Process
import threading
import time


def handler(Q):
    TransOfDay.append(Q)


def listener(WeatherTab):
    print("Starting Thread :", threading.current_thread().name)
    Q = TransactionsMarket.get()
    gestion = threading.Thread(target=handler, args=(Q))


class worker(Process):
    def __init__(self, lock, name):
        super().__init__()
        self.lock = lock
        self.name = name

    def run(self):
        print("starting thread :", self.name)

        while True:
            time.sleep(1)
            print("J'ai fini de travailler")
            lock.acquire()
            lock.release()


        print("Ending thread :", threading.current_thread().name)

if __name__ == "__main__":

    TransactionsMarket = Queue()
    thread = threading.Thread(target=listener, args=())
    TransOfDay = list()

    lock = threading.Lock()

    trav1 = worker(lock, "trav1")
    trav2 = worker(lock, "trav2")

    trav1.start()
    trav2.start()

    for i in range(0,5):
        print("Début du jour",i,"------------------------")
        lock.acquire()
        time.sleep(3)
        #Calcul du nouveau prix
        lock.release()