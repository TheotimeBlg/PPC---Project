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

    def __init__(self, name, HomesQueue, GeneralQueue):
        super().__init__()
        self.name = name
        self.HomesQueue = HomesQueue
        self.GeneralQueue = GeneralQueue
        self.Px = 0
        self.Cx = 0
        self.Policy = random.randint(1, 3)
        print(self.name, "est de type", self.Policy)

    def donne(self, Q):
        message = str(Q).encode()
        HomesQueue.put(message)
        print(self.name, "donne ses ", Q, "Energie.")

    def vend(self, Q):
        print(self.name, "vend au market",Q,"Energie !")

    def achete(self, Q):
        try:
            print(self.name, "essaie d'avoir de l'energie gratuite...")
            don = int(HomesQueue.get(True, 2))

            if don > -Q:
                print(self.name, "prend", don, "Energie et remet", don + Q, "Energie dans la queue.")
                self.donne(don+Q)
            elif don < -Q:
                print(self.name, "prend", don, "Energie, mais ça ne suffit pas ! Il lui manque", Q + don, "Energie.")
                self.achete(Q+don)
            else:
                print(self.name, "prend", don, "Energie dans la file ! Merci <3")

        except Exception as e:
            print(e)
            print("No givers !")
            print(self.name, "achète au market", Q, "Energie !")

    def giver(self, Q):
        if Q > 0:
            self.donne(Q)
        elif Q < 0:
            self.achete(Q)
        else:
            print(self.name, "ne fais rien.")

    def seller(self, Q):
        if Q > 0:
            self.vend(Q)
        elif Q < 0:
            self.achete(Q)
        else:
            print(self.name, "fais rien.")

    def middle(self, Q):
        if Q > 0:
            if HomesQueue.empty():
                print("il n'y a pas de dons en cours")
                self.donne(Q)
            else:
                print(self.name, "n'a pas besoin de donner, il y a déjà des dons en cours !")
                self.vend(Q)
        elif Q < 0:
            self.achete(Q)
        else:
            print(self.name, "ne fais rien")

    switcher = {
        1: giver,
        2: seller,
        3: middle,
    }

    def run(self):

        print("starting thread :", self.name)

        a = time.time()
        timeOut = 0
        while timeOut < 1000:
            b = time.time()
            timeOut = b-a

            if Flag.value == 1:
                self.Px = random.randint(1, 20)
                self.Cx = random.randint(1, 20)
                Q = self.Px - self.Cx
                print(Q)

                func = self.switcher.get(self.Policy, "")
                func(self, Q)
                time.sleep(1)

        print("Ending thread :", self.name)



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
    maFile = Queue()

    def afficheQueue(maFile):

        copy = []
        i = 0

        print("-------------------------------------------------")
        while not maFile.empty():
                n = maFile.get()
                print("| ", n.decode(), "", end='')
                copy.append(n)
                i += 1
        for k in range(len(copy)):
            maFile.put(copy[k])
        print(" |\n-------------------------------------------------")


    HomesQueue = Queue()
    GeneralQueue = Queue() #File de messages pour les achats/ventes
    WeatherTab = Array('i', range(2))
    iteration= Value('i', 1) #iteration est implémenté à chaque fois que meteo est lancé. Il intervient dans le calcul de la température

    # Pour la synchro :
    Flag = Value('i', 0)

    #initialisation
    WeatherTab[0]=21

    maison1 = Home("maison1", HomesQueue, GeneralQueue)
    maison2 = Home("maison2", HomesQueue, GeneralQueue)
    maison3 = Home("maison3", HomesQueue, GeneralQueue)
    weather = Meteo(WeatherTab, iteration, Flag, "Meteo")

    maison1.start()
    maison2.start()
    maison3.start()
    weather.start()

    time.sleep(1)

    for i in range(0, 4):
        print("")
        print("Début du jour ", i, "---------------------------------------------------")
        print("La température est de", WeatherTab[0], "degrés celcius", "et il fait le temps", WeatherTab[1], "\n")
        Flag.value = 1
        time.sleep(0.1)  # Pendant ce temps on veut être sûrs que tous les threads sont lancés (mais n'ont pas encore fini !)
        Flag.value = 0
        time.sleep(5)   # Pendant ce temps on veut être sûrs que tons les threads ont fini.
        afficheQueue(HomesQueue)


    maison1.join()
    maison2.join()
    maison3.join()
    weather.join()
