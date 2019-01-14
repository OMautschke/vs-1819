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
    UID_temp_n = 0
    UID_temp_nn = 0

    def __init__(self, id):
        self.UID = id
        self.UID_temp = id
        self.State = ProcessState.ACTIVE
        print("Process " + str(self.UID) + " inited")

    def send(self, q):
        state = "ACTIVE"
        if self.State == ProcessState.RELAY:
            state = "RELAY"
        print ("Process " + str(self.UID) + " - " + state)
        q.append(self.UID_temp)

    def receive(self, q, mem):
        if mem == 1:
            self.UID_temp_n = q.popleft()
        else:
            self.UID_temp_nn = q.popleft()

    def checkSend(self, q, elected):
        if self.UID_temp_n == self.UID:
            elected = self.UID
        else:
            if self.UID_temp > self.UID_temp_n:
                q.append(self.UID_temp)
            else:
                q.append(self.UID_temp_n)
        return elected

    def final(self, elected):
        if self.UID_temp_nn == self.UID:
            elected = self.UID
        else:
            if self.UID_temp_n >= self.UID_temp_nn and self.UID_temp_n >= self.UID_temp:
                self.UID_temp = self.UID_temp_n
            else:
                self.State = ProcessState.RELAY
        return elected

    def getState(self):
        return self.State


def main():
    print("Simulation started")
    print("Init...")
    id = 0
    elected = -1
    sharedMemory = deque([])
    numProcesses = int(sys.argv[1])
    processes = []
    for i in range(0, numProcesses):
        processes.append(Process(id))
        id = id + 1

    while True:
        processes[0].send(sharedMemory)
        for p in range(1, numProcesses):
            processes[p].receive(sharedMemory, 1)
            processes[p].send(sharedMemory)
        processes[0].receive(sharedMemory, 1)

        elected = processes[0].checkSend(sharedMemory, elected)
        for p in range(1, numProcesses):
            processes[p].receive(sharedMemory, 2)
            elected = processes[p].checkSend(sharedMemory, elected)
            if elected > -1:
                break
        if elected > -1:
            break
        processes[0].receive(sharedMemory, 2)

        for p in range(0, numProcesses):
            elected = processes[p].final(elected)
            if elected > -1:
                break
        if elected > -1:
            break
    print("Process " + str(elected) + " was elected!")


if __name__ == "__main__":
    main()