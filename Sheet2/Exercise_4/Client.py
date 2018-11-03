

def callback(batch_size, elapsed_time):
    print(batch_size, " primes calculated in", elapsed_time, " seconds")


if __name__ == "__main__":
    import rpyc
    c = rpyc.connect("localhost", 18861)
    lower, upper = 1, 1000000
    print("\n### Starting request ...")
    list_of_primes = c.root.get_primes(lower, upper, callback)
    print("### Received {} primes".format(len(list_of_primes)))
