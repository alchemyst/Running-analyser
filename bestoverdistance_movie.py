import matplotlib.pyplot as plt
import seaborn
import pandas
import numpy
from glob import glob
import functools
import os
import sys
from tqdm import tqdm

@functools.lru_cache(None)
def loaddata(filename):
    data = numpy.loadtxt(filename)

    if len(data.shape) == 2:
        distances = data[:, 0]
        times = data[:, 1]
        speeds = distances/times*(1/1000*60*60)
        paces = 60/speeds

    return distances/1000, speeds

def plotcurve(track, typ, line, *args, **kwargs):
    filename = 'bests/{}_{:04d}.dat'.format(typ, track)
    try:
        distances, speeds = loaddata(filename)
    except:
        return

    if line is None:
        plt.semilogx(distances, speeds, *args, **kwargs)
    else:
        line.set_data(distances, speeds)

markers = [5, 10, 21, 42]

def setup_axis():
    fix, ax = plt.subplots()

    date = plt.text(5, 25, 'This is the date', fontsize=20)
    thisrun, = plt.semilogx([0, 10], [0, 2], color='blue', zorder=10)
    bestsofar, = plt.semilogx([0, 10], [0, 2], color='red', linewidth=2, zorder=10)

    plt.xlabel('Distance / km')
    plt.ylabel('Speed / km/h')

    plt.ylim([0, 30])
    plt.xlim([0.1, 60])

    for marker in markers:
        plt.axvline(marker, alpha=0.2, zorder=10)

    return ax, date, thisrun, bestsofar

def addtrack(track, date, thisrun, bestsofar, thedate):
    plotcurve(track, 'track', None, color='k', alpha=0.05)
    plotcurve(track, 'track', thisrun)
    plotcurve(track, 'upto', bestsofar)
    date.set_text(thedate)

def makepng(track):
    filename = '{:04d}.png'.format(track)
    plt.savefig(filename)

if __name__ == "__main__":
    tracks = pandas.read_csv('tracks.csv', names=['tracki', 'track'], index_col='tracki')
    runhistory = pandas.read_table('history.dat', index_col=0, sep=' ', names=['track', 'date', 'distance'])

    ax, date, thisrun, bestsofar = setup_axis()

    for track in tqdm(list(tracks.track)):
        thedate = runhistory.loc[track].date
        addtrack(track, date, thisrun, bestsofar, thedate)
        makepng(track)
