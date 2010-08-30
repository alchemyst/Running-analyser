#!/usr/bin/env python

import numpy
import scipy.stats
import csv
import progressbar

def findbesttime(t, d, targets):
    bests = numpy.inf*targets
    for i in range(len(t)-1):
        thesetimes = numpy.interp(targets, d[i+1:]-d[i], t[i+1:]-t[i],
                                  right=numpy.inf)
        bests = numpy.minimum(thesetimes, bests)
    return bests

def writebests(filename, distances, bests):
    ofile = file(filename, 'w')
    for (d, b) in zip(distances, bests):
        if numpy.isfinite(b):
            print >> ofile, d, b
    print >> ofile

def hms(secs):
    """ Calculate hours minutes and seconds from seconds """
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    return (h, m, s)
    
# suck in data
print "Reading data"
rundata = numpy.recfromcsv('allruns.csv')
distances = numpy.loadtxt('watchdistances.dat')
maxdistance = max(rundata['distance'])
distances = distances[distances <= maxdistance]

# process
bests = numpy.inf*distances
runset = set(rundata["track"])
widgets = ['Analysing: ',
           progressbar.Percentage(),
           ' ', progressbar.Bar("="), ' ', progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets, maxval=max(runset)).start()

besthistory = numpy.zeros([len(runset), len(distances)])
for tracki, track in enumerate(sorted(runset)):
    trackdata = rundata[rundata['track']==track]
    trackbests = findbesttime(trackdata['seconds'], trackdata['distance'],
                              targets=distances)
    bests = numpy.minimum(trackbests, bests)
    besthistory[tracki, :] = bests
    writebests('bests/upto_%04i.dat'%track, distances, bests)
    writebests('bests/track_%04i.dat'%track, distances, trackbests)
    pbar.update(track)
besth = file('besthistory.dat', 'w')
numpy.savetxt('besthistory.dat', besthistory.T)
writebests('bestoverdistance.dat', distances, bests)
pbar.finish()

# Figure out how we are doing compared to world records
records = numpy.loadtxt('records.dat')
# interpolate the watchdistances in the records file
watchrecords = numpy.interp(distances, records[:,0], records[:,1])
# geometric mean better for fractions
fworldrecords = scipy.stats.gmean(watchrecords/bests)
flasttobest = 1/scipy.stats.gmean(filter(numpy.isfinite, trackbests/bests))
print "We are doing %2.1f%% of world records" % (fworldrecords*100)
print "Last run was %2.1f%% of best" % (flasttobest*100)

# show where we did well
newbests = numpy.arange(len(bests))[bests == trackbests]
if len(newbests) > 0:
    print "New bests:"
    for track in newbests:
        h, m, s = hms(bests[track])
        ph, pm, ps = hms(bests[track]/distances[track]*1000.0)
        print "%2.1fm\t%ih%02i:%02i\t%2i:%02i min/km" % (distances[track], h, m, s, pm, ps)

# Add results for last run
distances = list(distances)
trackbests = list(trackbests)
distances.append(trackdata['distance'][-1])
trackbests.append(trackdata['seconds'][-1] - trackdata['seconds'][0])
distances, trackbests = zip(*sorted(zip(distances, trackbests)))

writebests('lastrun.dat', distances, trackbests)
