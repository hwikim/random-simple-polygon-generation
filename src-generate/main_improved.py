# -----------------------------------------------------------------------------
#   Improved polygon generation algorithm
# -----------------------------------------------------------------------------

from src.Edge import Edge
from src.Polygon import Polygon
from src.Math import quickhull, pnt2line

import heapq
import sys
import matplotlib.pyplot as plt
import time

import json
import generate
import partition
import sys

if __name__ == "__main__":

    #m = int(input("number of problem instances: "))
    #sizePart = int(input("Size of the partition: "))
    #minSizeSubpoly = int(input("Minimum size of each subpolygon: "))

    # m = 1
    # sizePart = 3
    # minSizeSubpoly = 5

    filename = sys.argv[1]
    sizePart = int(sys.argv[2])
    minSizeSubpoly = int(sys.argv[3])

    #for j in range(m):

        #if j != m-1:
        #    continue

    f = open("./" + filename, "r")

    #f = open("test" + generate.twoDigit(j) + ".txt", "r")

    # take input from test.txt
    # f = open("test.txt", "r")

    # start timer
    start = time.time()

    # insert input points to list
    points = []
    n = int(f.readline())
    for i in range(n):
        coord = f.readline().split(' ')
        points.append([float(coord[0]), float(coord[1])])

    # initialize the polygon as a convex hull of the points
    polygon = Polygon(quickhull(points))

    # update points set to exclude polygon vertices
    points = [x for x in points if x not in polygon.vertices]

    # initialize MinPQ, dictionary
    distances = []
    heapq.heapify(distances)
    distancesDict = {}

    # pre-process by adding the distances between every edge-point pair into MinPQ and dictionary
    for edge in polygon.edges:
        for point in points:
            curr_dist = pnt2line(point, edge.start, edge.end)
            heapq.heappush(distances, curr_dist)
            distancesDict[curr_dist] = (edge, point)

    # iterate so long as there still exist points in the interior
    while points and len(distances) != 0:

        # get the current shortest distance and its corresponding edge-point pair
        curr_dist = heapq.heappop(distances)
        e = distancesDict[curr_dist][0]
        point = distancesDict[curr_dist][1]

        # check if the edge exists in the current polygon
        containsE = False
        for edge in polygon.edges:
            if e.start == edge.start and e.end == edge.end:
                containsE = True

        # proceed only if edge is in polygon, point is in interior, and it is a
        # valid addition to the polygon
        if containsE and point in points and e.valid(polygon, point):
            # get index of the edge
            for edge in polygon.edges:
                if e.start == edge.start and e.end == edge.end:
                    i = polygon.edges.index(edge)
            # insert new edges and point into the polygon,
            # remove old edge from polygon and remove point from interior
            polygon.vertices.insert(i + 1, point)
            polygon.edges[i] = Edge(e.start, point)
            polygon.edges.insert(i + 1, Edge(point, e.end))
            points.remove(point)
            # update MinPQ by adding distances between two new edges
            # and every point in interior
            e1 = Edge(e.start, point)
            e2 = Edge(point, e.end)
            for point in points:
                curr_dist_e1 = pnt2line(point, e1.start, e1.end)
                curr_dist_e2 = pnt2line(point, e2.start, e2.end)
                heapq.heappush(distances, curr_dist_e1)
                heapq.heappush(distances, curr_dist_e2)
                distancesDict[curr_dist_e1] = (e1, point)
                distancesDict[curr_dist_e2] = (e2, point)

    # print results
    print()
    print("--------------- Improved Approach --------------")
    print("Number of vertices:  %i" % n)
    print("Execution time:      %s seconds" % (time.time() - start))
    print("------------------------------------------------")
    print()

    # plt.figure(figsize=(6, 8))

    # plot the polygon
    originalPset = polygon.vertices

    psets, diagonals = partition.partition(originalPset, sizePart, minSizeSubpoly)

    psets2, _ = partition.partition(originalPset)
    # f = open("polygon" + generate.twoDigit(j) + ".txt", "w")
    #
    #
    # for _ in pset:
    #     first, second = _
    #     f.write(first + ' ' + second)

    numPlotsPerAxis = 1
    while numPlotsPerAxis**2 < len(psets)+1:
        numPlotsPerAxis += 1

    f, axes = plt.subplots(numPlotsPerAxis, numPlotsPerAxis, sharex = True, sharey = True)

    f.set_figheight(15)
    f.set_figwidth(15)

    # plt.sharex()

    plt.xlim([0, 1])
    plt.ylim([0, 1])

    oriPoly = psets2[0]

    oriPoly.append(oriPoly[0])
    # oriPolyVers = []

    # list of vertices
    versL = []

    for p in oriPoly:
        versL.append([p.x, p.y])

    xs, ys = zip(*versL)
    axes[0,0].plot(xs, ys)

    # diagonalVers = []
    for d in diagonals:
        dPoints = []
        for p in d:
            dPoints.append([p.x, p.y])

        # diagonalVers
        xs, ys = zip(*dPoints)
        axes[0,0].plot(xs, ys)
        # for d in diagonals:

    for idPset in range(len(psets)):
        pset = psets[idPset]
        pset.append(pset[0])

        psetVers = []
        for p in pset:
            psetVers.append([p.x, p.y])

        xs, ys = zip(*psetVers)
        axes[(idPset+1) // numPlotsPerAxis,(idPset+1) % numPlotsPerAxis].plot(xs, ys)

    data = {}
    data['id'] = "random" # + generate.twoDigit(j)

    data['container'] = {}
    data['container']['x'] = []
    data['container']['y'] = []

    for i in range(len(versL)-1):
        data['container']['x'].append(versL[i][0])
        data['container']['y'].append(versL[i][1])

    data['items'] = []

    # each subpolygon in the partition
    for i in range(len(psets)):
        dic = {}
        # dic['x'] = []
        # dic['y'] = []

        dic['id'] = i

        pset = psets[i]

        psetVers = []
        for p in pset:
            psetVers.append([p.x, p.y])

        del psetVers[-1]

        xs, ys = zip(*psetVers)

        dic['x'] = xs
        dic['y'] = ys

        data['items'].append(dic)


    # filePath = "./data" + generate.twoDigit(j) + ".json"
    filePath = filename + ".json"

    with open(filePath, 'w') as outfile:
        json.dump(data, outfile, indent=2)

    #mng = plt.get_current_fig_manager()
    #mng.window.state("zoomed")


    plt.show()

    # close test.txt file
    # f.close()

# plt.show()