#!/usr/bin/env python

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt
import argparse
import sys

parser = argparse.ArgumentParser(description='Plot run positions')
parser.add_argument('filename', type=argparse.FileType('r'),
                    help='The filename to be parsed (expects a CSV)')
parser.add_argument('--grouping',
                    help='Grouping to use')
parser.add_argument('-o', '--outfile',
                    help='Output filename')
parser.add_argument('--filterfield',
                    help='Field to filter on')
parser.add_argument('--filtervalue',
                    help='Filter value')
parser.add_argument('--highlightfield', default='Surname',
                    help='Field to highlight on')
parser.add_argument('--highlightvalue', default='Sandrock',
                    help='Value to highlight')
parser.add_argument('--title',
                    help='Title of chart')
args = parser.parse_args()

d = pandas.read_csv(args.filename, parse_dates=['Time'], index_col='Time')

if args.filterfield:
    d = d[d[args.filterfield] == args.filtervalue]

for key, group in d.groupby(args.grouping.split(',')):
    subset = group[args.highlightfield].str.contains(args.highlightvalue)

    positions = numpy.arange(1, len(group)+1)
    print(key)
    plt.plot(group.index, positions, label=' '.join(key))
    if any(subset):
        plt.scatter(group.index[subset],
                    positions[numpy.array(subset)],
                    color='red')
plt.ylim(ymin=0)
plt.legend(loc='best')
plt.ylabel('Position in group')
plt.xlabel('Time (hh:mm:ss)')
if args.title:
    plt.title(args.title)
if args.outfile:
    plt.savefig(args.outfile)
else:
    plt.show()
