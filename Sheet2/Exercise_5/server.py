#!/usr/bin/env python3
#server
import rpyc
import time

def primes(lowerLimit, upperLimit, batchSize, cbfunc):
    primes = []
    bT = True #bT = boolTrue
    elapsed = 0.0
    batch = 0
    
    start_time = time.time()
    for possiblePrime in range(lowerLimit, upperLimit+1):
        #Assume a number is prime until shown it is not
        isPrime = True
        for num in range(2, int(possiblePrime**0.5)+1):
            if possiblePrime % num == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(possiblePrime)
            batch += 1 #batch is the length of primes
            if (batch % batchSize == 0): # one batch of primes == batchSize
                stop_time = time.time()
                elapsed = stop_time - start_time 
                cbfunc(batch, elapsed)

    return primes

class MyService(rpyc.Service):
    def on_connect(self, conn): #runs when a connection is started
        print("\n>>> RPyC service connected ....")

    def on_disconnect(self, conn): #runs after the connection has closed
        print("<<< RPyC service disconnected ...")

    def exposed_get_primes(self, lowerLimit, upperLimit, callbackF): #exposed method
        print(" Starting computation on server ..")
        list_of_primes = primes(lowerLimit, upperLimit, 1000, callbackF)
        print(" Computing finished.")
        return list_of_primes

if __name__ == "__main__":
    from rpyc.utils.server import ForkingServer
    t = ForkingServer(MyService, port=18861)
    t.start()

