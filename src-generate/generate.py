# -----------------------------------------------------------------------------
#   Randomly generate points in a [0,1) x [0,1) square and write to test.txt
# -----------------------------------------------------------------------------

import sys
import random

def twoDigit(i):
    if i > 10:
        return str(i)
    else:
        return '0' + str(i)


if __name__ == "__main__":

    m = int(input("Number of problem instances: "))

    # prompt user to enter the number of vertices
    n = int(input("Number of vertices: "))

    for j in range(m):

        f = open("test" + twoDigit(j) + ".txt", "w")
        f.write("%i\n" % n)
        for i in range(n):
            x = random.random()
            y = random.random()
            f.write("%f %f\n" % (x, y))
        f.close()
