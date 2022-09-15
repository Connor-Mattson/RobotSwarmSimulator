import random

import numpy as np


def printArrayAsCSV(array_like):
    outstr = ""
    for i in range(len(array_like) - 1):
        outstr += str(round(array_like[i], 5)) + ", "
    outstr += str(round(array_like[-1], 5))
    print(outstr)


# Change this line depending on the genome space you want to augment
GENOME = [0.89235, 0.70532, -0.0868, 0.34489]

THRESHOLD = 0.05
SAMPLE_COUNT = 3
MIN_VALUE = -1.0
MAX_VALUE = 1.0
INCL_SUBTRACTION = True

for _ in range(SAMPLE_COUNT):

    addr = np.array([0.0 for j in GENOME])
    for i in range(len(addr)):
        addr[i] = ((random.random() * THRESHOLD * 2) - THRESHOLD)

    plus = GENOME + addr
    plus = np.array([max(MIN_VALUE, min(MAX_VALUE, val)) for val in plus])

    printArrayAsCSV(plus)
    printArrayAsCSV(-1 * plus)
    if INCL_SUBTRACTION:
        minus = GENOME - addr
        minus = np.array([max(MIN_VALUE, min(MAX_VALUE, val)) for val in minus])
        printArrayAsCSV(minus)
        printArrayAsCSV(-1 * minus)
