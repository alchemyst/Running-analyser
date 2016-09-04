#!/usr/bin/env python

import sqlite3
import numpy
import csv
import sys
import time


# On the mac this is linked to
# ~/Library/Application Support/Garmin/Training Center/Training Center.gtc
if len(sys.argv) > 1:
    database = sys.argv[1]
else:
    database = "Training Center.gtc"

# The Training center uses an epoch of 1 January 2001
# FIXME: this doesn't handle the time zone info correctly -- this should be in UTC
garminepoch = time.mktime((2001, 1, 1, 0, 0, 0, 0, 0, 0))

# TODO: Don't query on zimagename
trackquery = """select zTrack,zdisplayedname from zCDTreeItem where zActivity2 in (select known.value from known_runvalues as known where known.type='run') order by zStartTime3 asc"""
pointquery = """select zTime, ifNull(zHeartRate, 0), zCumulativeDistance, ifNull(zCadence, 0)
from zCDTrackPoint join zCDTRackSegment on zCDTrackPoint.zBelongsToTrackSegment=zCDTrackSegment.z_PK
where zCDTrackSegment.zBelongsToTrack=? and zCumulativeDistance is not null
order by zTime asc"""
rawnames = ['time', 'heartrate', 'distance', 'cadence']
rawformats = ['i8', 'i2', 'f8', 'i2']
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
    if any(e==None for e in fp):
        return numpy.array([0 for i in x])
    else:
        return numpy.interp(x, xp, fp)
        
def splitruns(results):
    longtime = 10*60*60 # this is considered a long time between points - new run
    t = results["time"]
    dt = numpy.diff(t)
    splits = numpy.array(numpy.nonzero(dt>longtime))
    splits = numpy.insert(splits, [0, splits.size], [-1, t.size])
    for startindex, endindex in zip(splits[:-1], splits[1:]):
        #print startindex+1, endindex
        yield results[startindex+1:endindex]
        
con = sqlite3.connect(database)
cur = con.execute(trackquery)
    
allruns = csv.writer(open('allruns.csv', 'w'))
histogram = open('histogram.dat', 'w')
runhistory = open('history.dat', 'w')

allruns.writerow(["track"] + writenames)

rnumber = 0
tracknames = set()

badtracks = set()

for (track,name,) in cur:
    if track is None:
        print("problem with %s (no track number)" % (name))
        continue
    elif name in tracknames:
        print("skipping %s (already processed)" % (name))
        badtracks.add(track)
        continue
    else:
        print("processing %s (track %i)" % (name, track))

    tracknames.add(name)
    
    cur2 = con.execute(pointquery, (track,))
    t = cur2.fetchall()
    if len(t) > 3:
        queryresult = numpy.rec.fromrecords(t, names = rawnames, formats=rawformats)
        for raw in splitruns(queryresult):
            #print (raw['time'][-1] - raw['time'][0])/60./60.
            rnumber += 1
            raw['distance'] -= raw['distance'][0] # correct distance for runs not starting at 0
            if numpy.any(raw['distance']>2e5):
                print(" - strangely long distance (%3.1f km) detected, skipping." % numpy.max(raw['distance']/1000))
                continue
            
            # interpolate data to once a second
            seconds = numpy.arange(raw['time'][0], raw['time'][-1])
            interp = lambda v: noneinterp(seconds, raw['time'], v)
            try:
                interped = numpy.rec.fromarrays([interp(raw[m]) for m in interpnames],
                                                names=interpnames)
            except:
                for m in interpnames:
                    print(m, raw[m].dtype)
            speed = 3.6 * numpy.diff(interped['distance']);
            smoothspeed = ewma(0.93, speed)
    
            if numpy.any(speed>50):
                print(" - fast speed (max=%2.1f) detected, skipping." % numpy.max(speed))
                continue
            if not numpy.all(numpy.isfinite(speed)):
                print(" - non-finite speed. skipping.")
                continue
    
            # note starting date and distance in log
            starttime = time.gmtime((raw['time'][0] + garminepoch))
            datestr = time.strftime("%Y-%m-%d", starttime)
            print(rnumber, datestr, numpy.max(raw['distance']), file=runhistory)
            
            for i in range(len(seconds)-1):
                row = [rnumber, seconds[i], 
                       interped['heartrate'][i], 
                       interped['distance'][i], 
                       speed[i], smoothspeed[i], 
                       interped['cadence'][i]]
                allruns.writerow(row)
    
            # generate speed histogram
            (counts,edges) = numpy.histogram(smoothspeed, bins=nbins, range=histrange, normed=True)
            for (c,e) in zip(counts, edges):
                print(rnumber, e, c, file=histogram)
            print(file=histogram)

#    print

print(badtracks)
