import random


#initialisation :
Px = randomInt(1,20)
Cx = randomInt(1,20)

Policy = randomInt(1,3)
#1 = Donne toujours
#2 = Vend toujours
#3 = Essaye de donner, sinon Vend

key = 128

boolean flag


MarketQueue = sysv_ipc.MessageQueue(key)
#type 1 => Donne
#type 2 => Vend
#type 3 => Achete

while flag =! True:
    Q = Px - Cx


    if Q > 0:
        cas 1:
            Donne(Q)
        cas 2:
            Vend(Q)
        cas 3:
            try:
                Donne(Q)
            except NoTakers:
                Vend(Q)
    elif Q < 0:
        Achete(Q)
    else:

    flag = False


def Donne(Q): #doit lever une exception si notre don n'est pas accepté dans un temps imparti


    message = str(Q).encode()
    MarketQueue.send(message, block = True, type = 1)




def Vend(Q):
    message = str(Q).encode()
    MarketQueue.send(message, block = True, type = 2)

def Achete(Q):
    Thread.sleep(10) #optionnel, pour attendre que les maisons aient mis leur dons dans la file
    try:
        message, t = MarketQueue.receive(block = False, type = 1)

        valeur = int(message.decode())
        if valeur > Q:
            Reste = valeur - Q
            Donne(Reste)
        elif valeur < Q:
            Reste = Q - valeur
            Achete(Reste)
    except:
        message, t = MarketQueue.send(block = False, type = 3)
