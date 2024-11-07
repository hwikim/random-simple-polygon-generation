# the algorithm recursively partitions the given polygon

import matplotlib.pyplot as plt
import random
import generate
import copy
import math

# A Python3 program to find if 2 given line segments intersect or not

class Point:
    def __init__(self, x, y, oriID = None, pos = None):
        self.x = x
        self.y = y
        # vertex id of the original polygon
        self.oriID = oriID
        self.ID = oriID
        # position
        # -1 for dummy
        # 00 for vertex, 10 for edge Steiner point that is contained in the current diagonal,
        # 20 for interior Steiner point)
        self.pos = pos

    #  edge Steiner point일 때 edge index
    def setPrevNext(self, prev, next):
        self.prev = prev
        self.next = next

    def initializePrevNext(self):
        self.prev = None
        self.next = None

    def makePosZero(self):
        self.pos = 0

    def changeID(self, newID):
        self.ID = newID

    # Given three collinear points p, q, r, the function checks if

epsStandard = 0.1**10

# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


def getAB(ver1, ver2):
    x0 = ver1.x
    y0 = ver1.y
    x1 = ver2.x
    y1 = ver2.y

    if x1 == x0:
        return None, None

    A = (y1-y0)/(x1-x0)
    B = y0 - (y1-y0)*x0/(x1-x0)
    return A, B

def newIntersect(ver1, ver2, ver3, ver4):
    A, B = getAB(ver1, ver2)
    C, D = getAB(ver3, ver4)

    x = None
    # Both parallel to the y-axis
    if A == None and C == None:
        yIntersect = (max(ver1.y, ver2.y) <= min(ver3.y, ver4.y) or
                    max(ver3.y, ver4.y) <= min(ver1.y, ver2.y))
        yIntersect = not yIntersect

        if ver1.x == ver3.x and yIntersect:
            return True
        else:
            return False
    elif A == None:
        x = ver1.x

    elif C == None:
        x = ver3.x

    elif A == C:
        xIntersect = (max(ver1.x, ver2.x) <= min(ver3.x, ver4.x) or
                    max(ver3.x, ver4.x) <= min(ver1.x, ver2.x))
        xIntersect = not xIntersect

        if B == D and xIntersect:
            return True
        else:
            return False

    else:
        x = (D-B) / (A-C)

    if (ver1.x < x < ver2.x or ver2.x < x < ver1.x) and (ver3.x < x < ver4.x or ver4.x < x < ver3.x):
        return True
    else:
        return False

def newIntersectIncident(ver1, ver2, ver3, ver4):
    A, B = getAB(ver1, ver2)
    C, D = getAB(ver3, ver4)

    x = None
    # Both parallel to the y-axis
    if A == None and C == None:
        yIntersect = (max(ver1.y, ver2.y) < min(ver3.y, ver4.y) or
                    max(ver3.y, ver4.y) < min(ver1.y, ver2.y))
        yIntersect = not yIntersect

        if ver1.x == ver3.x and yIntersect:
            return True
        else:
            return False
    elif A == None:
        x = ver1.x

    elif C == None:
        x = ver3.x

    elif A == C:
        xIntersect = (max(ver1.x, ver2.x) < min(ver3.x, ver4.x) or
                    max(ver3.x, ver4.x) < min(ver1.x, ver2.x))
        xIntersect = not xIntersect

        if B == D and xIntersect:
            return True
        else:
            return False

    else:
        x = (D-B) / (A-C)

    if (ver1.x <= x <= ver2.x or ver2.x <= x <= ver1.x) and (ver3.x <= x <= ver4.x or ver4.x <= x <= ver3.x):
        return True
    else:
        return False

# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def isDiagonalIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    # if ((o1 == 0) and onSegment(p1, p2, q1)):
    #     return True
    #
    # # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    # if ((o2 == 0) and onSegment(p1, q2, q1)):
    #     return True
    #
    # # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    # if ((o3 == 0) and onSegment(p2, p1, q2)):
    #     return True
    #
    # # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    # if ((o4 == 0) and onSegment(p2, q1, q2)):
    #     return True

    # If none of the cases
    return False

# def isValidDiagonal(vers, id1, id2):
#     ver1 = vers[id1]
#     ver2 = vers[id2]

def intersect(ver1, ver2):
    pass
    # find the intersection point

def incrementMod(num, mod):
    if num == mod - 1:
        return 0
    else:
        return num + 1

def decrementMod(num, mod):
    if num == 0:
        return mod - 1
    else:
        return num

def modDifference(a, b, mod):
    if a > b:
        temp = a
        a = b
        b = temp

    # mod 7일 때, 1과 6의 거리는 2
    return min(b - a, a + mod - b)

# check if P1 lies inside the polygon 'vers'
def isInsidePol(vers, P1, P2):

    crossing = 0

    for i in range(len(vers)):
        j = incrementMod(i, len(vers))

        if newIntersect(P1, P2, vers[i], vers[j]):
            crossing += 1

    if crossing % 2 == 0:
        return False
    else:
        return True

def perturbedP(P1, P2, _pos = -1, eps = epsStandard):
    return Point(P1.x + (P2.x - P1.x) * eps, P1.y + (P2.y - P1.y) * eps, pos = _pos)

def perturbedPval(x1, y1, x2, y2, eps = epsStandard):
    return x1 + (x2 - x1) * eps, y1 + (y2 - y1) * eps

# Checking if a point is inside a polygon
def point_in_polygon(point, polygon):
    num_vertices = len(polygon)
    x, y = point.x, point.y
    inside = False

    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]

    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1.y, p2.y):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1.y, p2.y):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1.x, p2.x):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if p1.x == p2.x or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        p1 = p2

    # Return the value of the inside flag
    return inside

# 주어진 line segment가 diagonal을 구성할 수 있는지 판단
def isIntersecting(vers, P1, P2, diagonal):
    Q1 = perturbedP(P1, P2, -1)
    Q2 = perturbedP(P2, P1, -1)

    for i in range(len(vers)):
        j = incrementMod(i, len(vers))

        if newIntersect(Q1, Q2, vers[i], vers[j]):
            return True

    if len(diagonal) >= 2:
        for i in range(len(diagonal)):
            j = incrementMod(i, len(diagonal))

            v1 = perturbedP(diagonal[i], diagonal[j])
            v2 = perturbedP(diagonal[j], diagonal[i])

            if newIntersect(Q1, Q2, v1, v2):
                return True

    return False

# def isOutside()

def getBoundaryPoint(vers, id, probVer = 0.5):
    # vertex
    if random.random() < probVer:
        if vers[id].pos == 20:
            pass
        return vers[id]

    # edge (which connects the (startID)-th vertex and the (startID+1)-th vertex
    # 자를 때는 잘 보이도록, 0.3에서 0.7 사이 위치에서.
    else:
        id2 = incrementMod(id, len(vers))

        v1 = vers[id]
        v2 = vers[id2]

        edgeCutPos = 0.3 + random.random() * 0.4

        ret = perturbedP(v1, v2, 10, edgeCutPos)
        ret.setPrevNext(id, id2)

        return ret

# input: vertices (list of list)
def partition(vers, sizePart=1, minSizeSubpoly=10000):
    minStepMove = 0.05
    maxStepMove = 0.3

    maxNumIterations = 1000
    numIterations =  0

    maxNumSteiner = 10
    extP = Point(2.0, 2.0)

    # ex)
    diagonals = []

    # vector of points
    oriPoly = []

    for i in range(len(vers)):
        oriPoly.append(Point(vers[i][0], vers[i][1], i, 0))

    polys = [oriPoly]
    # numPoly = 1

    indexChosen = -1

    # on the vertex with probability 0.5
    probVer = 0.5
    # thus, on the interior of an edge with probability 0.5

    endProb = 0.0
    # 중간 step에서만 적용됨
    # 절대 값 or subpolygon size에 상대적인 값? 현재는 절대.

    for i in range(sizePart-1):

        # current diagonal


        P1 = None
        P2 = None
        curD = []

        while True:

            indexChosen = random.randint(0, len(polys) - 1)
            vers = polys[indexChosen]
            numVers = len(vers)

            startID = random.randint(0, numVers - 1)

            curD = [getBoundaryPoint(vers, startID)]

            finishFlag = False

            while True:
                numIterations += 1

                if numIterations >= maxNumIterations:
                    numIterations = 0
                    if minSizeSubpoly > 4:
                        minSizeSubpoly -= 1
                    print('minSizeSubPoly now ' + str(minSizeSubpoly))

                if len(curD) == maxNumSteiner:

                    for endID in range(len(curD)):
                        # (1) min size 조건
                        if modDifference(startID, endID, numVers) < minSizeSubpoly:
                            continue

                        # boundary 위의 점을 확정
                        # endpoint candidate
                        candP = getBoundaryPoint(vers, endID)

                        # (2) validity(nonintersecting) 조건
                        # 지금까지의 diagonal과도 교차하지 않아야 함
                        if isIntersecting(vers, curD[-1], candP, curD):
                            continue

                        # (3) inside 조건
                        if not isInsidePol(vers, perturbedP(curD[-1], candP), extP):
                            continue

                        curD.append(candP)
                        finishFlag = True
                        break

                    break

                # 끝 step: boundary에 몸 담고 마침
                elif random.random() < endProb:
                    endID = random.randint(0, numVers - 1)


                    # (1) min size 조건
                    if modDifference(startID, endID, numVers) <  minSizeSubpoly:
                        continue

                    # boundary 위의 점을 확정
                    # endpoint candidate
                    candP = getBoundaryPoint(vers, endID)

                    # (2) validity(nonintersecting) 조건
                    # 지금까지의 diagonal과도 교차하지 않아야 함
                    if isIntersecting(vers, curD[-1], candP, curD):
                        continue

                    # (3) inside 조건
                    if not isInsidePol(vers, perturbedP(curD[-1], candP), extP):
                        continue

                    curD.append(candP)
                    finishFlag = True
                    break
                    # curD.append()

                # 중간 step: polygon 내부에 Steiner point를 생성
                else:

                    # (1) min size 조건은 여기서 고려할 필요 없음

                    # random move

                    stepMove = minStepMove + random.random() * (maxStepMove - minStepMove)

                    randomRad = random.random() * 2 * math.pi

                    # (next) Steiner point candidate
                    candP = Point(curD[-1].x + stepMove * math.cos(randomRad), curD[-1].y + stepMove * math.sin(randomRad), 20)

                    # (2) validity(nonintersecting) 조건
                    # 지금까지의 diagonal과도 교차하지 않아야 함
                    if isIntersecting(vers, curD[-1], candP, curD):
                        # print('Cannot place the Steiner point. Intersecting')
                        continue

                    # (3) inside 조건
                    if not isInsidePol(vers, perturbedP(curD[-1], candP), extP):
                        # print('Cannot place the Steiner point. Outside of the polygon')
                        continue

                    # print('Placed the Steiner point successfully')
                    curD.append(candP)

                if finishFlag:
                    break

            if finishFlag:
                break

        diagonals.append(curD)

        print("diagonal size: " + str(len(curD)))
        print('diagonal vertices: ', end=' ')
        for p in curD:
            print('(' + str(p.x) + ', ' + str(p.y) + ')', end=' ')
        print()

        # vertex면 제거 (subpolygon에서 vertex가 중복되지 않도록)
        copyD = copy.deepcopy(curD)
        if copyD and copyD[0].pos == 0:
            del copyD[0]
        if copyD and copyD[-1].pos == 0:
            del copyD[-1]

        reverseD = copy.deepcopy(copyD)
        reverseD.reverse()

        # (new) start of subpolygon 1
        sp1s = curD[0].ID
        # (new) end of subpolygon 1
        sp1e = curD[-1].ID

        sp2s = curD[-1].ID
        sp2e = curD[0].ID

        if curD[0].pos // 10 == 1:
            sp1s = curD[0].next
            sp2e = curD[0].prev

        if curD[-1].pos // 10 == 1:
            sp1e = curD[-1].prev
            sp2s = curD[-1].next

        if sp1s == None or sp2s == None:
            pass

        if sp1e == None or sp2e == None:
            pass

        subPoly1Indices = [sp1s]
        subPoly2Indices = [sp2s]

        while True:
            q = incrementMod(subPoly1Indices[-1], numVers)
            subPoly1Indices.append(q)
            if q == sp1e:
                break

        while True:
            q = incrementMod(subPoly2Indices[-1], numVers)
            subPoly2Indices.append(q)
            if q == sp2e:
                break

        subPoly1 = []
        for id in subPoly1Indices:
            subPoly1.append(copy.deepcopy(vers[id]))

        # diagonal 더해주기
        subPoly1 += reverseD

        subPoly2 = []
        for id in subPoly2Indices:
            subPoly2.append(copy.deepcopy(vers[id]))

        subPoly2 += copyD

        for i in range(len(subPoly1)):
            subPoly1[i].changeID(i)
            subPoly1[i].makePosZero()
            subPoly1[i].initializePrevNext()

        for i in range(len(subPoly2)):
            subPoly2[i].changeID(i)
            subPoly2[i].makePosZero()
            subPoly2[i].initializePrevNext()

        polys.append(subPoly1)
        polys.append(subPoly2)

        del polys[indexChosen]

        print('deleted polygon size: ' + str(len(vers)))
        print('subpolygon 1 size: ' + str(len(subPoly1)), end = ', ')
        print('subpolygon 1 indices: ', end = ' ')
        print(*subPoly1Indices)
        print('subpolygon 2 size: ' + str(len(subPoly2)), end = ', ')
        print('subpolygon 2 indices: ', end = ' ')
        print(*subPoly2Indices)
        print()

    return polys, diagonals

if __name__ == "__main__":
    pass
    # size of the partition
    # sizePart = int(input("Size of the partition: "))

    # numInstances = int(input("Number of instances: "))
    #
    # for i in range(numInstances):
    #     f = open("test" + generate.twoDigit(i) + ".txt", "r")



