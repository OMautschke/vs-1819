#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import matplotlib.pyplot as plt


def isStable(bPrivilege):
    #print(bPrivilege)
    counter = 0
    for i in range(len(bPrivilege)):
        if(bPrivilege[i]): counter += 1

    if counter > 1:
        return False
    else:
        return True

def dijkstra_token_ring(node, i, K):
    global states
    if i != 0:
        bPrivilege[i] = False
        if (node[i] != node[i-1]):
            node[i] = node[i-1]
            bPrivilege[(i+1)%K] = True
            states += 1

    else:
        bPrivilege[0] = False
        if (node[0] == node[len(node)-1]):
            node[0] += 1 % K
            bPrivilege[1] = True
            states += 1

if __name__ == '__main__':
    stepsN = [None]*500 #Average steps per run N
    statesN = [None]*500 #Average number of changed states per run N

    for N in range(500, 1000):
        steps = 0
        states = 0
        bPrivilege = [True]*N #At the beginning, assume every node is privileged
        K = 4

        for k in range(15):
            node = [random.randint(0, K) for _ in range(N)]
            while(not isStable(bPrivilege)):
                #print(not isStable(bPrivilege))
                dijkstra_token_ring(node, random.randint(0,N-1), K)
                steps += 1
        stepsN[N-500] = steps/15
        statesN[N-500] = states/15
        print("Average steps: ", stepsN[N-500])
        print("Average state changes: ", statesN[N-500])
        print("---------------------------")
    plt.figure(1, figsize=(30, 10))
    plt.subplot(131)
    plt.plot([y for y in range (500, 1000)], stepsN)
    plt.ylabel('Average steps taken')
    plt.xlabel('number of N')
    plt.subplot(132)
    plt.plot([y for y in range (500, 1000)], statesN)
    plt.ylabel('Average states changed')
    plt.xlabel('number of N')
    plt.show()
"""
1. Average steps for N = 20: ~16, less than N for each N
2. Average state changes: ~3.5, much less than N for each N
3. Average steps and state changes are very random
"""