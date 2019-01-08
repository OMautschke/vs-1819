from enum import Enum
from collections import deque
import sys
import time
from random import randint

class MsgType(Enum):
    REPLY = 1
    REQUEST = 2

class ProcessMessage:
    msgType = 0
    timestamp = 0
    id = 0

    def __init__(self, t, stamp, id):
        self.timestamp = stamp
        self.msgType = t
        self.id = id

class ProcessState(Enum):
    RELEASED = 1
    WANTED = 2
    HELD = 3

class Process:
    ID = 0
    Clock = 0
    State = 0
    Recieved = deque([])
    Queued = deque([])
    numReplies = 0
    numProcesses = 0
    reqStamp = 0

    def __init__(self, id, numProcesses):
        self.ID = id
        self.State = ProcessState.RELEASED
        self.Clock = 0
        self.numReplies = 0
        self.numProcesses = numProcesses
        print("Process " + str(self.ID) + " inited")

    def broadcastRequest(self, processes):
        print("Process " + str(self.ID) + " is sending a broadcast")
        for i in range (0, self.numProcesses - 1):
            if i == self.ID:
                continue
            processes[i].Recieved.append(ProcessMessage(MsgType.REQUEST, self.Clock, self.ID))
            self.Clock += 1

    def enterCriticalSection(self, processes):
        if self.State != ProcessState.WANTED:
            print("Process " + str(self.ID) + " tries to enter critical section")
            self.broadcastRequest(processes)
            self.reqStamp = self.Clock
        self.State = ProcessState.WANTED
        if self.numReplies == self.numProcesses - 1:
            self.numReplies = 0
            self.State = ProcessState.HELD
            print("Process " + str(self.ID) + " is in the critial section!")

    def reply(self, processes):
        while (len(self.Recieved) > 0):
            m = self.Recieved.popleft()
            if m.timestamp > self.Clock:
                self.Clock = m.timestamp
            if  (m.msgType == MsgType.REQUEST):
                if self.State == ProcessState.HELD or (self.State == ProcessState.WANTED and self.reqStamp >= m.timestamp):
                    processes[m.id].Recieved.append(ProcessMessage(MsgType.REPLY, self.Clock, self.ID))
                    self.Clock += 1
                    print("Process " + str(self.ID) + ": Message send to " + str(m.id))
                else:
                    self.Queued.append(m)
                    print("Process " + str(self.ID) + ": Message queued")
            else:
                self.numReplies += 1

    def exitCriticalSection(self, processes):
        print("Process " + str(self.ID) + " exits critical section")
        self.State = ProcessState.RELEASED
        while (len(self.Queued) > 0):
            m = self.Queued.popleft()
            if m.timestamp > self.Clock:
                self.Clock = m.timestamp
            processes[m.id].Recieved.append(ProcessMessage(MsgType.REPLY, self.Clock, self.ID))
            self.Clock += 1


    def run(self, processes):
        self.reply(processes)
        if self.State == ProcessState.HELD and randint(0, 3) == 0:
            self.exitCriticalSection(processes)
        elif randint(0, 9) == 0 or self.State == ProcessState.WANTED:
            self.enterCriticalSection(processes)

def main():
    print("Simulation started")
    print("Init...")
    id = 0
    numProcesses = 16#int(sys.argv[1])
    processes = []
    for i in range (0, numProcesses):
        processes.append(Process(id, numProcesses))
        id = id + 1

    for s in range (0, 10000):
        for p in range (0, numProcesses):
            processes[p].run(processes)


if __name__ == "__main__":
    main()
