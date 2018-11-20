#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import numpy as np
from pyspark import SparkContext

def parseVector(line):
    return np.array([float(x) for x in line.split('')])

def distanceCentroidsMoved(oldCentroids, newCentroids):
    sum = 0.0
    for index in range(len(oldCentroids)):
        sum += np.sum((oldCentroids[index] - newCentroids[index])**2)
    return sum

def closestPoint(p, centroids):
    bestIndex = 0
    closest = float("+inf")
    for index in range(len(centroids)):
        tempDist = np.sum((p - centroids[index])**2)
        if tempDist < closest:
            closest = tempDist
            bestIndex = index
    return bestIndex

if __name__ == "__main__":
    sc = SparkContext(appName="PythonKMeans")
    lines = sc.textFile(sys.argv[1])
    data = lines.map(parseVector).cache()

    k = int(sys.argv[2])

    centroids = data.takeSample(False, k, 1)
    newCentroids = centroids[:]

    convergeDist = float(sys.argv[3])

    tempDist = 2*convergeDist
    while tempDist > convergeDist:
        closest = data.map(lambda p: (closestPoint(p, centroids), (p,1)))
        for cIndex in range (k):
            closestOneCluster=closest.filter(lambda d: d[0] == cIndex).map(lambda d: d[1])

            sumAndCountOneCluster=closestOneCluster.reduce(
                    lambda p1, p2: (p1[0]+p2[0], p1[1]+p2[1]))
            vectorSum = sumAndCountOneCluster[0]
            count = sumAndCountOneCluster[1]
            newCentroids[cIndex] = vectorSum / count

        tempDist = distanceCentroidsMoved(centroids, newCentroids)
        centroids = newCentroids[:]