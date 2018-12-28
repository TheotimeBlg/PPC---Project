import random
from multiprocessing import Array, Process



 #tab: shared memory qui prend en premier argument la température entre -10 et 40°
 #et en deuxième argument un entier 1,2 ou 3 (1 : soleil / 2: pluie ou nuage / 3: neige)

def weather(tab):
    tab[0]=random.randrange(-10,40)
    tab[1]=random.randrange(1,4)


if __name__=='__main__':
    WeatherTab = Array('i', range(2))

    weather = Process(target=weather, args=(WeatherTab,))
    weather.start()
    weather.join()

    print("la température est de : ",WeatherTab[0]," il fait le temps ",WeatherTab[1])
