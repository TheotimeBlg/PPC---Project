import random
import random
import time
import math
from multiprocessing import Process, Queue, Array, Value
import threading

global  Pt #prix à l'instant t
global  fi #contribution à l'instant t de la météo
global  mu # ={0,1} 0: pas d'evenement externe 1 : un évenement externe
global  Beta #coefficient de modulation des evenements exterieurs


class Home(Process):

    def __init__(self):
        super().__init__()
        self.Px = 0
        self.Cx = 0
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
            print("J'essaie d'avoir de l'energie gratuite")
            don = int(HomesQueue.get(True, 2))

            if don > Q:
                self.donne(don-Q)
                print("J'ai pris", Q, "Energie et j'ai remis", don-Q, "Energie dans la queue")
            elif don < Q:
                self.achete(Q-don)
                print("J'ai pris", Q, "Energie, mais ça ne suffit pas ! Il me manque", Q-don, "Energie.")
            else:
                print("J'ai pris", Q, "Energie dans la file ! Merci <3")

        except Exception as e:
            print(e)
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
            if HomesQueue.empty():
                print("il n'y a pas de dons en cours")
                self.donne(Q)
            else:
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
        self.Px = random.randint(1, 20)
        self.Cx = random.randint(1, 20)
        Q = self.Px - self.Cx
        print(Q)

        func = self.switcher.get(self.Policy, "")
        func(self, Q)


class Meteo(Process):

    def __init__(self, WeatherTab, iteration, drapeau, name):
        super().__init__()
        self.WeatherTab = WeatherTab
        self.iteration = iteration
        self.Flag = drapeau
        self.name = name


    def run(self):

        print("starting thread :", self.name)

        a = time.time()
        timeOut = 0
        while timeOut < 1000:

            b = time.time()
            timeOut = b-a

            if self.Flag.value == 1:
                # Récupération des anciennes valeurs de WeatherTab avant modification et calcul de alpha de manière aléatoire
                t = self.WeatherTab[0]
                alpha = random.randrange(-4, 4)

                with self.iteration.get_lock():
                    self.iteration.value += 1

                T = (t + math.cos(0.1*iteration.value)*alpha)   #La nouvelle température est calculée à partir de l'ancienne température, d'un paramètre alpha aléatoire et d'un paramètre w implémenté de 1 à chaque appel de run
                self.WeatherTab[0] = int(T)

                if T < 0:
                    WeatherTab[1] = random.randint(1, 3) #1 : Soleil    2 : Nuage    3 : Neige
                else:
                    WeatherTab[1] = random.randint(1, 2)    #il ne peut pas neiger si T>0°


                time.sleep(0.2)

        print("Ending thread :", self.name)



if __name__ == "__main__":

    HomesQueue = Queue()
    GeneralQueue = Queue() #File de messages pour les achats/ventes
    WeatherTab = Array('i', range(2))
    iteration= Value('i', 1) #iteration est implémenté à chaque fois que meteo est lancé. Il intervient dans le calcul de la température

    # Pour la synchro :
    Flag = Value('i', 0)

    #initialisation
    WeatherTab[0]=21

    #maison1 = Home(HomesQueue, GeneralQueue)
    #maison2 = Home(HomesQueue, GeneralQueue)
    weather = Meteo(WeatherTab, iteration, Flag, "Meteo")

    #maison1.start()
    #maison2.start()
    weather.start()

    time.sleep(1)

    for i in range(0, 40):
        print("")
        print("Début du jour ", i, "---------------------------------------------------")
        print("La température est de", WeatherTab[0], "degrés celcius", "et il fait le temps", WeatherTab[1], "\n")
        Flag.value = 1
        time.sleep(0.1)
        Flag.value = 0
        time.sleep(1)
        #maison1.run()
        #maison2.run()
        #weather.run()

    #maison1.join()
    #maison2.join()
    weather.join()
