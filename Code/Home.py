import random
import time
from multiprocessing import Queue



class Home(Process):

    def __init__(self, HomesQueue, GeneralQueue):
        super().__init__()
        self.Px = 0
        self.Cx = 0
        self.HomesQueue=HomesQueue
        self.GeneralQueue=GeneralQueue
        self.Policy = random.randint(1, 3)      # 1 = donne toujours     # 2 = vend toujour    # 3 = essaie de donner, vend sinon
        print("Je suis de type", self.Policy)

    def donne(self, Q):
        message = str(Q).encode()
        self.HomesQueue.put(message)
        print("J'ai donné mes ", Q,"Energie")

    def vend(self, Q):
        message = str(Q).encode()
        self.GeneralQueue.put(message)
        print("Je vends au market",Q,"Energie !")

    def achete(self, Q):
        try:
            Q=math.fabs(Q) #on travaille avec la valeur absolue de Q car on sait pertinament que Q<0
            print("J'essaie d'avoir de l'energie gratuite")
            don = int(self.HomesQueue.get(True, 2).decode()) #Reste bloqué pendant 2 secondes pour essayer d'avoir de l'énergie gratuite

            if don > Q:
                self.donne(don-Q)
                print("J'ai pris", Q, "Energie et j'ai remis", don-Q, "Energie dans la queue")
            elif don < Q:
                self.achete(-Q+don)
                print("J'ai pris", don, "Energie, mais ça ne suffit pas ! Il me manque", -Q+don, "Energie.")
            else:
                print("J'ai pris", Q, "Energie dans la file ! Merci <3")

        except Exception as e:
            print("No givers !")
            self.GeneralQueue.put(str(Q).encode())
            print("J'achète au market", Q, "Energie !")

    def giver(self, Q):
        if Q > 0:
            self.donne(Q)
        elif Q < 0:
            self.achete(Q)
        else:
            print("Je ne fais rien.")

    def seller(self, Q):
        if Q > 0:
            self.vend(Q)
        elif Q < 0:
            self.achete(Q)
        else:
            print("Je ne fais rien.")

    def middle(self, Q):
        # - BALANCE TON DON
        # - sleep(10 sec)
        # - get(QUE AVEC TON PID) exceptions
        # - Si pas d'exception tu vend
        # - sinon Fin

        if Q > 0:
            if HomesQueue.empty():
                print("il n'y a pas de dons en cours")
                self.donne(Q)
            else:
                print("Pas besoin de donner, il y a déjà des dons en cours !")
                self.vend(Q)
        elif Q < 0:
            self.achete(Q)
        else:andom.randint(1, 20)
    switcher = {
        1: giver,
        2: seller,
        3: middle,
    }

    def run(self):
        while True :
            self.Px = random.randint(1, 20)
            self.Cx = random.randint(1, 20)
            Q = self.Px - self.Cx
            print(Q)


            func = self.switcher.get(self.Policy, "")
            func(self, Q)

            mutex.acquire()


if __name__ == "__main__":
    switcher = {
        1: giver,
        2: seller,
        3: middle,
    }


    Flag = True

    while Flag:
        Q = Px - Cx

        func = switcher.get(Policy, "")
        func(Q)

    Flag = False
