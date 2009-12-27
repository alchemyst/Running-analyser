#!/usr/bin/env python

import numpy
import scipy.stats
import csv
import progressbar

def recfromcsv(filename):
    """Returns a record array from a CSV."""
    # TODO: unnecessary in new numpy > 1.3.1
    c = csv.reader(file(filename))
    headers = c.next()
    data = [map(float, row) for row in c]
    return numpy.rec.fromrecords(data, names=headers)

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
rundata = recfromcsv('allruns.csv')
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

for track in sorted(runset):
    trackdata = rundata[rundata['track']==track]
    trackbests = findbesttime(trackdata['seconds'], trackdata['distance'],
                              targets=distances)
#    writebests('bestoverdistance_%04i.dat'%track, distances, trackbests)
    bests = numpy.minimum(trackbests, bests)
    pbar.update(track)
writebests('bestoverdistance.dat', distances, bests)
pbar.finish()

# Figure out a factor for distances

# FIXME: this weights the shorter distances more because there are
# more points
records = numpy.loadtxt('records.dat')
# interpolate the watchdistances in the records file
watchrecords = numpy.interp(distances, records[:,0], records[:,1])
# geometric mean better for fractions
f = scipy.stats.gmean(watchrecords/bests)
# f = float(numpy.linalg.lstsq(numpy.matrix(bests).T,
#                              numpy.matrix(watchrecords).T)[0])

print "We are doing %2.1f%% of world records" % (f*100)

# show where we did well
newbests = numpy.arange(len(bests))[bests == trackbests]
if len(newbests) > 0:
    print "New bests:"
    for track in newbests:
        h, m, s = hms(bests[track])
        ph, pm, ps = hms(bests[track]/distances[track]*1000.0)
        print "%track\t%ih%02i:%02i\t%2i:%02i min/km" % (distances[track], h, m, s, pm, ps)

# Add results for last run
distances = list(distances)
trackbests = list(trackbests)
distances.append(trackdata['distance'][-1])
trackbests.append(trackdata['seconds'][-1] - trackdata['seconds'][0])
distances, trackbests = zip(*sorted(zip(distances, trackbests)))

writebests('lastrun.dat', distances, trackbests)
