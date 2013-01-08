#!/usr/bin/env python

import sys

def seconds(timestr):
    return reduce(lambda a, b: a*60+b,
                  [float(t) for t in timestr.split(':')])

for line in sys.stdin:
    items = line.split('\t')
    distance = items[0]
    times = [str(seconds(i)) for i in items[1:]]
    print '\t'.join([distance] + times)
