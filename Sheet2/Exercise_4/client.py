#!/usr/bin/env python3
#client

def callbackF(primes, sec):
    print("{} primes calculated in {} seconds".format(primes, sec))

if __name__ == "__main__":
    import rpyc
    # Parameter here: server-name/IP-adr, server-port
    c = rpyc.connect("localhost", 18861)

    lower, upper = 1000000, 3000000
    print("\n### Starting request ...")

    list_of_primes = c.root.get_primes(lower, upper, callbackF)

    print("### Received {} primes".format(len(list_of_primes)))
