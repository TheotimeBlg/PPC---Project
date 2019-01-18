import numpy as np
import random
import matplotlib.pyplot as plt
import time

def remplirTab(Tableau):
    Tableau.append(random.random()*1.145)


if __name__ == "__main__":

    tab = [0.145, 0.157, 0.168, 0.99, 0.132]

    plt.ylabel('Prix en euros par kWh')
    plt.xlabel('temps en jours')

    for i in range(0, 20):

        remplirTab(tab)
        plt.plot(tab)
        plt.scatter(i, tab[i])
        plt.pause(0.5)
    plt.show()