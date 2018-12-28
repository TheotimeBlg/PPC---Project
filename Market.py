import random
import time
from multiprocessing import Process, Queue, Array




class Home(Process):
    def __init__(self):
        print("Starting process :", Process.name)
        super().__init__()
        self.Px = random.randint(1, 20)
        self.Cx = random.randint(1, 20)
        self.Policy = random.randint(1, 3)
        print("Je suis de type", self.Policy)

    def donne(self, Q):
        message = str(Q).encode()
        HomesQueue.put(message)
        print("J'ai donné mes ", Q,"Energie")

    def vend(self, Q):
        print("Je vends au market",Q,"Energie !")

    def achete(self, Q):
        try:
            print("J'essaie d'avoir de l'energie gratuite mdr")
            HomesQueue.get(True, 1)
            print("Yes ")
        except :
            print("No givers !")
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
        if Q > 0:
            if HomesQueue.empty:
                self.donne(Q)
            else :
                print("Pas besoin de donner, il y a déjà des dons en cours !")
                self.vend(Q)
        elif Q < 0:
            self.achete(Q)
        else:
            print("Je ne fais rien")

    switcher = {
        1: giver,
        2: seller,
        3: middle,
    }

    def run(self):
        Q = self.Px - self.Cx

        func = self.switcher.get(self.Policy, "")
        func(self, Q)


class Weather(Process):
    def __init__(self, WeatherTab):
        print("Starting process Weather")
        super().__init__()

    def run(self):
        WeatherTab[0] = random.randint(-10,40)
        WeatherTab[1] = random.randint(1,3)


if __name__ == "__main__":

    HomesQueue = Queue()
    WeatherTab = Array('i', range(2))

    Meteo = Weather(WeatherTab)

    maison1 = Home()
    maison2 = Home()

    maison1.start()
    maison2.start()

    for i in range(0, 10):
        print("Début du jour ",i,"---------------------------------------------------")
        maison1.run()
        maison2.run()

    maison1.join()
    maison2.join()
