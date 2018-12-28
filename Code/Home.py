import random
import time


# initialisation

Px = random.randint(1, 20)
Cx = random.randint(1, 20)
Policy = random.randint(1, 3)
#1 = donne toujours
#2 = vend toujours
#3 = essaie de donner, vend sinon


def giver(Q):
    if Q > 0:
        print("Je donne", Q,"Energie !")
    elif Q < 0:
        print("J'achète au market", Q,"Energie")
    else:
        print("Je ne fais rien.")

def seller(Q):
    if Q > 0:
        print("Je vends au market",Q,"Energie !")
    elif Q < 0:
        print("J'achète au market",Q,"Energie !")
    else:
        print("Je ne fais rien.")

def middle(Q):
    if Q > 0:
        try:
            print("J'essaie de donner mes", Q,"Energie")
        except :
            print("Pas besoin d'énergie ! Je vend au market mes",Q,"Energie")
    elif Q < 0:
        print("J'achète au market",Q,"Energie")
    else:
        print("Je ne fais rien")



if __name__ == "__main__":
    switcher = {
        1: giver,
        2: seller,
        3: middle,
    }

    Flag = True

    while Flag:
        Q = Px - Cx

        func = switcher.get(Policy, "")
        func(Q)

    Flag = False