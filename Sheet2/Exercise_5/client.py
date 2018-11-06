#!/usr/bin/env python3
#client
import itertools
import sys
import time

def callbackF(primes, sec):
    print("{} primes calculated in {} seconds".format(primes, sec))

if __name__ == "__main__":
    import rpyc
    # Parameter here: server-name/IP-adr, server-port
    c = rpyc.connect("localhost", 18861)
    N = int(sys.argv[1]) # Number of intervals
    lower, upper = 1000000, 3000000
    list_of_primes = [None]*N
    interval = (upper - lower) // N
    
    elapsed = 0.0

    #bgsrv = rpyc.BgServingThread(c) 

    print("\n### Starting request ...")

    async_primes = rpyc.async_(c.root.get_primes)
    start_time = time.time()

    for i in range(N):
        if (i == N-1):
            list_of_primes[i] = async_primes(lower, upper, callbackF)
        else:
            list_of_primes[i] = async_primes(lower, lower + interval, callbackF)
            lower += interval
    b = False
    while(not b):
        for i in range(N):
            if list_of_primes[i].ready:
                b = True
            else:
                b = False
                break
    stop_time = time.time()
    elapsed = stop_time - start_time

    len_primes = 0
    for i in range(N):
        len_primes += len(list_of_primes[i].value)

    print("### Received {} primes in {} seconds".format(len_primes, elapsed))
    #bgsrv.stop()