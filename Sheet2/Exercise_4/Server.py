import rpyc
import time


class MyService(rpyc.Service):

    def on_connect(self, conn):
        print("\n>>> RPyC service connected ...")

    def on_disconnect(self, conn):
        print("<<< RPyC service disconnected ...")

    def exposed_get_primes(self, lower_limit, upper_limit, callback):
        print("    Starting computation on server .. ")
        list_of_primes = self.primes(lower_limit, upper_limit, callback)
        print("    Computing finished.“)")
        return list_of_primes

    def primes(self, lower_limit, upper_limit, callback):
        batch_size = 0
        primes = []
        start = time.time()
        for possible_prime in range(lower_limit, upper_limit + 1):
            is_prime = True
            for num in range(2, int(possible_prime ** 0.5) + 1):
                if possible_prime % num == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(possible_prime)
                batch_size += 1
                if len(primes) % 10000 == 0:
                    end = time.time()
                    callback(batch_size, end - start)

        return primes


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861, listener_timeout = 5000)
    t.start()