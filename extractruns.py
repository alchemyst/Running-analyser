#!/usr/bin/env python

import sqlite3
import string, os
import numpy
import csv
import sys

# On the mac this is linked to
# ~/Library/Application Support/Garmin/Training Center/Training Center.gtc
if len(sys.argv) > 1:
    database = sys.argv[1]
else:
    database = "Training Center.gtc"

trackquery = """select zTrack,zdisplayedname from zCDTreeItem where zImageName = 'history_running' order by zStartTime2 asc"""
pointquery = """select zTime, zHeartRate, zCumulativeDistance, zCadence
from zCDTrackPoint join zCDTRackSegment on zCDTrackPoint.zBelongsToTrackSegment=zCDTrackSegment.z_PK
where zCDTrackSegment.zBelongsToTrack=%i and zCumulativeDistance is not null and zHeartRate is not null
order by zTime asc"""
rawnames = ['time', 'heartrate', 'distance', 'cadence']
interpnames = [r for r in rawnames if r != 'time']
writenames = ['seconds', 'heartrate', 'distance', 'speed', 'smoothspeed', 'cadence']

histrange = (4, 14)
nbins = 25

def ewma(alpha, x):
    v = x[0]
    fx = x.copy()
    for i in range(len(x)):
        v = alpha*v + (1-alpha)*x[i]
        fx[i] = v 
    return fx

def noneinterp(x, xp, fp):
    if any([e==None for e in fp]):
        return numpy.array([0 for i in x])
    else:
        return numpy.interp(x, xp, fp)
        
con = sqlite3.connect(database)
cur = con.execute(trackquery)
    
allruns = csv.writer(file('allruns.csv', 'w'))
histogram = file('histogram.dat', 'w')
runhistory = file('history.dat', 'w')

allruns.writerow(["track"] + writenames)

rnumber = 0
tracknames = set()

for (track,name,) in cur:
    if track is None:
        print "problem with %s (no track number)" % (name)
        continue
    elif name in tracknames:
        print "skipping %s (already processed)" % (name)
        continue
    else:
        print "processing %s (track %i)" % (name, track)

    tracknames.add(name)
    
    cur2 = con.execute(pointquery % track)
    t = cur2.fetchall()
    if len(t) > 3:
        raw = numpy.rec.fromrecords(t, names = rawnames)
        rnumber += 1
        
        if numpy.any(raw['distance']>2e5):
            print " - strangely long distance (%3.1f km) detected, skipping." % numpy.max(raw['distance']/1000)
            continue
        
        # note starting date and distance in log
        print >> runhistory, raw['time'][0], numpy.max(raw['distance'])
        
        # interpolate data to once a second
        seconds = numpy.arange(raw['time'][0], raw['time'][-1])
        interp = lambda v: noneinterp(seconds, raw['time'], v)
        interped = numpy.rec.fromarrays([interp(raw[m]) for m in interpnames],
                                        names=interpnames)
        speed = 3.6 * numpy.diff(interped['distance']);
        smoothspeed = ewma(0.93, speed)

        if numpy.any(speed>40):
            print " - fast speed (max=%2.1f) detected, skipping." % numpy.max(speed)
            continue
#         if numpy.any(numpy.isfinite(speed)):
#             print " - non-finite speed. skipping."
#             continue

        for i in range(len(seconds)-1):
            row = [rnumber, seconds[i], interped['heartrate'][i], interped['distance'][i], speed[i], smoothspeed[i], interped['cadence'][i]]
            allruns.writerow(row)

        # generate speed histogram
        (counts,edges) = numpy.histogram(smoothspeed, bins=nbins, range=histrange, normed=True)
        for (c,e) in zip(counts, edges):
            print >> histogram, rnumber, e, c
        print >> histogram

#    print
