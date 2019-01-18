from multiprocessing import Queue, Process, Value
import threading
import time


def handler(Q):
    TransOfDay.append(int(Q))


def listener():
    print("Starting Thread :", threading.current_thread().name)
    while(True):
        Q = TransactionsMarket.get()
        print("hi : ", Q.decode())
        gestion = threading.Thread(target=handler, args=(Q.decode()))
        gestion.start()
        gestion.join()
        print("hola hola")


class worker(Process):
    def __init__(self, name, drapeau, TransactionsMarket):
        super().__init__()
        self.name = name
        self.Flag = drapeau
        self.TransactionsMarket=TransactionsMarket

    def run(self):
        print("starting thread :", self.name)

        a = time.time()
        timeOut = 0

        while timeOut < 10000:
            b = time.time()
            timeOut = b-a
            if self.Flag.value == 1:
                Q=2                             #cadre exemple
                self.TransactionsMarket.put(str(Q).encode())       #cadre exemple
                time.sleep(1)
                print(self.name, "a fini de travailler")
        print("Ending thread :", self.name)


if __name__ == "__main__":

    print("starting thread :", threading.current_thread().name)
    TransactionsMarket = Queue()
    TransOfDay = list()
    thread = threading.Thread(target=listener, args=())
    thread.start()

    Flag = Value('i', 0)

    trav1 = worker("trav1", Flag, TransactionsMarket)
    trav2 = worker("trav2", Flag, TransactionsMarket)

    trav1.start()
    trav2.start()

    Ptmoins1=0.145  # initialisation du prix au temps t moins-1

    for i in range(0,5):
        print("Début du jour", i, "------------------------")
        Flag.value = 1
        time.sleep(0.1) # Pendant ce temps on veut être sûrs que tous les threads sont lancés (mais n'ont pas encore fini !)
        Flag.value = 0
        time.sleep(3)   # Pendant ce temps on veut être sûrs que tons les threads ont fini.
        compteur=0
        print("TransOfDay", TransOfDay)
        for j in range(len(TransOfDay)):
            compteur=compteur+TransOfDay[j]
        print(compteur)

        #Calcul du nouveau prix

        gamma = 1.0-(compteur/100) #le coefficient est modifiée en fonction de ce qui a été vendu ou acheté au market. Plus on a acheté, plus le prix monte
        print("gamma ", gamma)
        Pt = gamma*Ptmoins1
        print("Le prix actuel est ", Pt)
        Ptmoins1=Pt

        TransOfDay=[] #on vide TransOfDay


    print("Ending thread :", threading.current_thread().name)
    thread.join()
