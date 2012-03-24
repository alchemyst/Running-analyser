#!/usr/bin/env python

import numpy
import scipy.stats
import csv
import progressbar
import tabulate

def findbesttime(t, d, targets):
    """Find best times over target distances

    Given a history of times and distances, figure out what the best
    times where for those distances with a sliding window
    interpolation.
    """
    # Start out thinking all are infinite
    bests = numpy.inf*targets
    # Loop through the time data
    for i in range(len(t)-1):
        # Interpolate the times for the target distances, as though
        # starting from this time step
        thesetimes = numpy.interp(targets, d[i+1:]-d[i], t[i+1:]-t[i], 
                                  right=numpy.inf)
        # Update bests
        bests = numpy.minimum(thesetimes, bests)
    return bests

def writebests(filename, distances, bests):
    ofile = file(filename, 'w')
    for (d, b) in zip(distances, bests):
        if numpy.isfinite(b):
            print >> ofile, d, b
    print >> ofile

def divparts(value, parts):
    """ Calculate a split of value into smaller units or parts.
    
    For instance, there are 60 seconds in a minute, 60 minutes in an hours and 24 hours in a day, so to split a number of seconds to seconds, minutes, hours, 
    days would be: 
    
    >> divparts(60*60*24+1, (60, 60, 24))
    [1, 0, 1]
    >> divparts(1234, (10, 10, 10))
    [4, 3, 2, 1]
    """
    retval = []
    for part in parts:
        [value, wholeparts] = divmod(value, part)
        retval.append(wholeparts)
    retval.append(value)
    return retval        

def hms(secs):
    """ Calculate hours minutes and seconds from seconds

    Obsolete: this should be replaced by divparts
    """
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    return (h, m, s)
    

def reportform(row):
    distance, lasttime, besttime = row
    if distance<1000:
        dstr = "%i m" % distance
    else:
        dstr = "%.2f km" % (distance/1000)
    s, m , h = divparts(lasttime, (60, 60))
    if h > 0:
        time = "%ih%02i:%02i" % (h, m, s)
    else:
        time = "%02i:%02i" % (m, s)
    speed = "%.2f" % ((distance/1000.0)/(lasttime/(60.0*60.0)))
    ps, pm = divparts(lasttime/distance*1000.0, (60,))
    pace = "%2i:%02i" % (pm, ps)
    star = "*" if lasttime == besttime else ""
    return dstr, time, speed, pace, star


def printbests(distances, times, besttimes=None):
    if besttimes is None:
        besttimes = times
    tabulate.printtable(headers=["Distance", "Time", "Speed", "Pace", ""],
                        data=zip(distances, times, besttimes),
                        rowformatter=reportform)

def main():
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
    
    numpy.savetxt('besthistory.dat', besthistory.T)
    writebests('bestoverdistance.dat', distances, bests)
    pbar.finish()
    
    # Figure out how we are doing compared to world records
    records = numpy.loadtxt('records.dat')
    # interpolate the watchdistances in the records file
    watchrecords = numpy.interp(distances, records[:, 0], records[:, 1])
    # geometric mean better for fractions
    fworldrecords = scipy.stats.gmean(watchrecords/bests)
    flasttobest = 1/scipy.stats.gmean(filter(numpy.isfinite, trackbests/bests))
    print "We are doing %2.1f%% of world records" % (fworldrecords*100)
    print "Last run was %2.1f%% of best" % (flasttobest*100)
    
    # show how we did:
    good = ~numpy.isinf(trackbests)
    printbests(distances[good], trackbests[good], bests[good])
    
    # Add results for last run
    distances = list(distances)
    trackbests = list(trackbests)
    distances.append(trackdata['distance'][-1])
    trackbests.append(trackdata['seconds'][-1] - trackdata['seconds'][0])
    distances, trackbests = zip(*sorted(zip(distances, trackbests)))
    
    writebests('lastrun.dat', distances, trackbests)

if __name__ == '__main__':
    main()