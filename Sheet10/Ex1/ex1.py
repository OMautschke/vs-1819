from enum import Enum
from collections import deque
import sys
import time
from random import randint

class ProcessState(Enum):
    ACTIVE = 1
    RELAY = 2

class Process:
    UID = 0
    State = 0
    UID_temp = 0

    def __init__(self, id):
        self.UID = id
        self.UID_temp = id
        self.State = ProcessState.ACTIVE
        print("Process " + str(self.UID) + " inited")
  
    def run(self, processes):
        state = "ACTIVE"
        if self.State == ProcessState.RELAY:
            state = "RELAY"
        print ("Process " + str(self.UID) + " - " + state)

def main():
    print("Simulation started")
    print("Init...")
    id = 0
    numProcesses = int(sys.argv[1])
    processes = []
    for i in range (0, numProcesses):
        processes.append(Process(id))
        id = id + 1

    for s in range (0, 10000):
        for p in range (0, numProcesses):
            processes[p].run(processes)


if __name__ == "__main__":
    main()
