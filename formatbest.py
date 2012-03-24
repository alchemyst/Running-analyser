#!/usr/bin/env python

import sys
import tabulate
from bestoverdistance import printbests

def load(filename):
    return zip(*[map(float, line.split()) for line in open(filename) if line.strip()])

if __name__ == '__main__':
    distances, times =  load(sys.argv[1])
    distances, besttimes = load('bestoverdistance.dat')
    printbests(distances, times, besttimes)