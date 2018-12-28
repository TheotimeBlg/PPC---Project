#Main principal

import external, weather, home



float Pt #prix à l'instant t
float PtMoins1 #Prix à l'instant t-1
float fi #contribution à l'instant t de la météo
int mu # ={0,1} 0: pas d'evenement externe 1 : un évenement externe
float Beta #coefficient de modulation des evenements exterieurs

class Weather(Process):
    #code de Weather
    def __init__(self):
        #...
    def run(self):
        #...


class External():
    #code de External
    def __init__(self):
        #...
    def run(self):
        #...

class home():
    #code de home
    def __init__(self, index):
        #...
    def run(self):
        #...


def workerHome(queue, data_ready, data):

    home = home(type_home) #type compris entre 1 et 3



if __name__ == "__main__":
    queue = Queue()
    creation_des_N_maisons(N, worker, queue, data_ready, data) #chaque maison = 1 thread
    w=Weather()
    e=external()

    







