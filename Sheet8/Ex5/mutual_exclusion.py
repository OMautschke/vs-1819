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
    stepsN = [None]*18 #Average steps per run N
    statesN = [None]*18 #Average number of changed states per run N

    for N in range(2, 20):
        steps = 0
        states = 0
        bPrivilege = [True]*N #At the beginning, assume every node is privileged
        K = N
        node = random.sample(range(K), N)
        for k in range(15):
            while(not isStable(bPrivilege)):
                #print(not isStable(bPrivilege))
                dijkstra_token_ring(node, random.randint(0,N-1), K)
                steps += 1
        stepsN[N-2] = steps/15
        statesN[N-2] = states/15
        print("Average steps: ", stepsN[N-2])
        print("Average state changes: ", statesN[N-2])
        print("---------------------------")
    plt.figure(1, figsize=(30, 10))
    plt.subplot(131)
    plt.plot([y for y in range (2, 20)], stepsN)
    plt.ylabel('Average steps taken')
    plt.xlabel('number of N')
    plt.subplot(132)
    plt.plot([y for y in range (2, 20)], statesN)
    plt.ylabel('Average states changed')
    plt.xlabel('number of N')
    plt.show()

