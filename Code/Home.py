import random
import time


# initialisation

Px = random.randint(1, 20)
Cx = random.randint(1, 20)
Policy = random.randint(1, 3)
# 1 = donne toujours
# 2 = vend toujours
# 3 = essaie de donner, vend sinon


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
