import random
from multiprocessing import Array, Process

class Weather(Process):
    def __init__(self):
        super().__init__()

    def run(self):
        WeatherTab[0] = random.randrange(-10, 40)
        WeatherTab[1] = random.randint(1, 3)


if __name__ == "__main__":

    WeatherTab = Array('i', range(2))

    meteo = Weather()

    meteo.start()

    for i in range(0,4):
        meteo.run()
        print("Jour",i,": il fait", WeatherTab[0], "degrés celcius et le temps est de", WeatherTab[1])
    meteo.join()

