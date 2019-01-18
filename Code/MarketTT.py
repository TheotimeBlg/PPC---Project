import random
import random
import time
import math
from multiprocessing import Process, Queue, Array, Value
import threading
import os
import signal

global  Pt #prix à l'instant t
global  fi #contribution à l'instant t de la météo
global  mu # ={0,1} 0: pas d'evenement externe 1 : un évenement externe
global  Beta #coefficient de modulation des evenements exterieurs


def GestionsHandler(Q):
    print("Starting Thread :", threading.current_thread().name)
    TransOfDay.append(float(Q))


def listener():
    print("Starting Thread :", threading.current_thread().name)
    while(True):
        Q = GeneralQueue.get()
        print("hi : ", Q.decode())
        gestion = threading.Thread(target=GestionsHandler, args=(Q.decode(),))
        gestion.start()
        gestion.join()


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
        message = str(Q).encode()
        self.GeneralQueue.put(message)
        print(self.name, "vend au market",Q,"Energie !")

    def achete(self, Q):
        try:
            Q=math.fabs(Q) #on travaille avec la valeur absolue de Q car on sait pertinament que si on achète alors Q<0
            print(self.name, "essaie d'avoir de l'energie gratuite...")
            don = int(self.HomesQueue.get(True, 2).decode()) #Reste bloqué pendant 2 secondes pour essayer d'avoir de l'énergie gratuite

            if don > Q:
                print(self.name, "prend", don, "Energie et remet", don - Q, "Energie dans la queue.")
                self.donne(don-Q)
            elif don < Q:
                print(self.name, "prend", don, "Energie, mais ça ne suffit pas ! Il lui manque", Q - don, "Energie.")
                self.achete(-Q+don)
            else:
                print(self.name, "prend", don , "Energie dans la file ! Merci <3")

        except Exception as e:
            print(e)
            print("No givers !")
            self.GeneralQueue.put(str(Q).encode())
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



class External(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name


    def run(self):
        while True:
            time.sleep(random.randint(1, 10))
            print("Choix du signal")
            cata = random.randint(1, 2)
            if cata == 1:
                os.kill(os.getppid(), signal.SIGUSR1) # 1 = Trouble social  (3 = pénurie matière première)
            elif cata == 2:
                os.kill(os.getppid(), signal.SIGUSR2) # 2 = Tension Diplomatique


if __name__ == "__main__":
    maFile = Queue()
    global Prix

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


    # Initialisation de prix TEMPORAIRE
    Prix = 100

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)

    HomesQueue = Queue()
    GeneralQueue = Queue() #File de messages pour les achats/ventes
    WeatherTab = Array('i', range(2))
    iteration= Value('i', 1) #iteration est implémenté à chaque fois que meteo est lancé. Il intervient dans le calcul de la température
    TransOfDay=list() #permettra de calculer le coefficient gamma du prix


    # Pour la synchro :
    Flag = Value('i', 0)

    #initialisation
    WeatherTab[0]=21
    Ptmoins1 = 0.145 #prix au temps t moins1
    somme=0 #sera utile par la suite pour calculer la somme des transactions de la journée

    maison1 = Home("maison1", HomesQueue, GeneralQueue)
    maison2 = Home("maison2", HomesQueue, GeneralQueue)
    maison3 = Home("maison3", HomesQueue, GeneralQueue)
    weather = Meteo(WeatherTab, iteration, Flag, "Meteo")
    ext = External("External")
    ListeningThread = threading.Thread(target=listener, args=())

    maison1.start()
    maison2.start()
    maison3.start()
    weather.start()
    ext.start()
    ListeningThread.start()

    global ExtPID       # Récupération du PID de external.
    ExtPID = ext.pid

    time.sleep(1)

    for i in range(0, 5):
        print("")
        print("Début du jour ", i, "---------------------------------------------------")
        print("La température est de", WeatherTab[0], "degrés celcius", "et il fait le temps", WeatherTab[1], "\n")
        Flag.value = 1
        time.sleep(0.1)  # Pendant ce temps on veut être sûrs que tous les threads sont lancés (mais n'ont pas encore fini !)
        Flag.value = 0
        time.sleep(5)   # Pendant ce temps on veut être sûrs que tons les threads ont fini.
        afficheQueue(HomesQueue)
        afficheQueue(GeneralQueue)

        #Calcul du prix

        #calcul la somme de l'ensemble des transactions de la journée
        for j in range(len(TransOfDay)):
            somme=somme+TransOfDay[j]
        #le coefficient gamma est modifiée en fonction de ce qui a été vendu ou acheté au market. Plus on a acheté, plus le prix monte
        gamma = 1.0-(somme/100)
        #prix actuel
        Pt = gamma*Ptmoins1
        print("Le prix actuel est :", Pt)
        print("Prix = ", Prix * ExternalValues[1])

        Ptmoins1=Pt
        TransOfDay=[] #on vide TransOfDay


    maison1.join()
    maison2.join()
    maison3.join()
    weather.join()
    ListeningThread.join()
