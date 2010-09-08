#!/usr/bin/env python

import sys

for line in sys.stdin:
    [distance, time] = line.split('\t')
    timeinseconds = reduce(lambda a, b: a*60+b,
                           [float(t) for t in time.split(':')])
    print distance, timeinseconds
