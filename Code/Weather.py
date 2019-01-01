import random
import math
from multiprocessing import Array, Process, Value


def runWeather(WeatherTab, iteration):
    #Récupération des anciennes valeurs de WeatherTab avant modification
    t= WeatherTab[0]
    alpha = random.randrange(-4, 4)
    iteration.value= iteration.value +1
    T= int(math.cos(iteration.value)*t*alpha)  #La nouvelle température est calculée à partir de l'ancienne température, d'un paramètre alpha aléatoire et d'un paramètre w implémenté de 1 à chaque appel de run
    WeatherTab[0] = T
    if (T<0) :
        WeatherTab[1] = random.randint(1, 3) #1 : Soleil    2 : Nuage    3 : Neige
    else :
        WeatherTab[1] = random.randint(1, 2)    #il ne peut pas neiger si T>0°


if __name__ == "__main__":
    WeatherTab = Array('i', range(2))
    iteration= Value('i', 1)

    #initialisation
    #WeatherTab[0]=21

    meteo = Process(target=runWeather, args=(WeatherTab, iteration))

    meteo.start()
    meteo.join()

    print(iteration.value)
    print(WeatherTab[:])
