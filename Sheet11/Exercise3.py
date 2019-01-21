import time
import datetime
import hashlib


LEADING_ZEROS = 3
NUM_OF_BLOCKS = 100


class Block:
    def __init__(self, index, prev_hash):
        self.index = index
        self.time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        self.nonce = 0
        self.prev_hash = prev_hash
        self.guess = 0

        self.proof_of_work()

    def proof_of_work(self):
        global NUM_OF_BLOCKS, LEADING_ZEROS
        self.nonce = 100 + self.index
        D = "0" * LEADING_ZEROS

        while True:
            hash = hashlib.sha256(("Hello World!" + str(self.nonce)).encode('utf-8'))
            self.guess += 1
            if D in str(hash.hexdigest()[:LEADING_ZEROS]):
                self.prev_hash = hash
                break
            self.nonce += 1

    def __str__(self):
        hash_string = str(self.prev_hash.hexdigest())
        return "Block: %s\n Time: %s\n Nonce: %s\n Previous Hash: %s\n" % (self.index, self.time_stamp, self.nonce, hash_string)


def main():
    # Part 1
    global NUM_OF_BLOCKS, LEADING_ZEROS
    block_chain = []

    guesses = 0
    start = time.time()
    for i in range(0, NUM_OF_BLOCKS):
        block_chain.append(Block(len(block_chain), block_chain[i - 1].prev_hash if i - 1 > -1 else 1))
        guesses += block_chain[i].guess
    end = time.time()

    print("Average guesses Blocks = 100; D = 3: " + str(int(guesses / NUM_OF_BLOCKS)))
    print("Time elapsed: " + str(end - start) + "\n")

    print(str(block_chain[0]))
    print(str(block_chain[1]))
    print(str(block_chain[2]))

    # Part 2
    block_chain = []
    NUM_OF_BLOCKS = 10
    LEADING_ZEROS = 4

    start = time.time()
    guesses = 0
    for i in range(0, NUM_OF_BLOCKS):
        block_chain.append(Block(len(block_chain), block_chain[i - 1].prev_hash if i - 1 > -1 else 1))
        guesses += block_chain[i].nonce
    end = time.time()

    print("Average guesses Blocks = 10; D = 4: " + str(int(guesses / NUM_OF_BLOCKS)))
    print("Time elapsed: " + str(end - start) + "\n")

    ##############################################################################################

    block_chain = []
    NUM_OF_BLOCKS = 10
    LEADING_ZEROS = 5

    start = time.time()
    guesses = 0
    for i in range(0, NUM_OF_BLOCKS):
        block_chain.append(Block(len(block_chain), block_chain[i - 1].prev_hash if i - 1 > -1 else 1))
        guesses += block_chain[i].nonce
    end = time.time()

    print("Average guesses Blocks = 10; D = 5: " + str(int(guesses / NUM_OF_BLOCKS)))
    print("Time elapsed: " + str(end - start) + "\n")


if __name__ == "__main__":
    main()
