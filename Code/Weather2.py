import random
import math
from multiprocessing import Process, Value, Array

class Meteo(Process):
    def __init__(self, WeatherTabtab, iteration):
        super().__init__()
        self.WeatherTab=WeatherTab
        self.iteration=iteration
    def run(self):
        #Récupération des anciennes valeurs de WeatherTab avant modification
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




if __name__ == "__main__":

    WeatherTab = Array('i', range(2))
    iteration = Value('d', 0)

    #initialisation
    WeatherTab[0]=21

    #Création du process meteo
    p = Meteo(WeatherTab, iteration)
    p.start()

    for i in range(0, 100):
        print("Jour ", i," : ")
        p.run()
        #print("iteration=",iteration.value)
        #print("Temperature",WeatherTab[:])

    p.join()
