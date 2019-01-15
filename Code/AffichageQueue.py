from multiprocessing import Queue, Process
import time


class worker(Process):
    def __init__(self, messageQueue):
        super().__init__()
        self.messageQueue = messageQueue


    def run(self):
        l = [1, 5, 7, 9, 15]
        for n in l:
            self.messageQueue.put(n)
            time.sleep(0.1)


if __name__ == "__main__":

    def afficheQueue(maFile):

        copy = []
        i = 0


        while not maFile.empty():
                n = maFile.get()
                print(i, "   ", n)
                copy.append(n)
                i += 1
        for k in range(len(copy)):
            maFile.put(copy[k])

    uneFile = Queue()

    worker1 = worker(uneFile)
    worker2 = worker(uneFile)

    worker1.start()
    worker2.start()

    worker1.join()
    worker2.join()

    afficheQueue(uneFile)

    afficheQueue(uneFile)

