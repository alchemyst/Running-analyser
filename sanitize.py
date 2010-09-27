#!/usr/bin/env python

# TODO: Check if multisport items are handled correctly (is there a chance of name collision?)

import sys
import sqlite3
import logging
logging.basicConfig(level=logging.INFO)

doit = True
if not doit: logging.warn('Not actually doing anything to the database')

dbfilename = "Training Center.gtc"
conn = sqlite3.connect(dbfilename)
conn.row_factory = sqlite3.Row

cur = conn.cursor()

# The key tables storing actual workout data points from device are
# zCDTrackPoint (many) -> (one) zCDTrackSegment (many) -> (one) zCDTrack
# The joins are on fields called zBelongsToX to the z_pk of each table.
#
# The zCDTreeItem table is used to store pretty much all the clickable
# stuff in the left hand window as well as lap info
# the entries with z_ent=41 have associated laps with z_ent=35 and link on zbelongstorun
#
# To get these numbers, do
# select distinct z_ent, zimagename from zcdtreeitem;
# z_ent   zimagename
#30    folder_courses
#30    folder_history
#30    folder_workout
#31    folder_history
#34    folder_myactivities
#35    {null}
#35    lap
#37    course
#38    multisport
#40    workout_biking
#40    workout_other
#40    workout_running
#41    history_biking
#41    history_other
#41    history_running

lapcode = 35
historycode = 41

# TODO: Rework all the del methods to duplicate less code
# Start with tables = ["Track", "TrackSegment", "TrackPoint"]

def deltrackpoint(cur, trackpoint_pk):
    logging.debug("Deleting trackpoint %i ..." % (trackpoint_pk,))
    if doit: cur.execute('delete from zCDTrackPoint where z_pk=?', (trackpoint_pk,))

def deltracksegment(cur, tracksegment_pk):
    logging.debug('Finding related trackpoints')
    cur.execute('select z_pk from zCDTrackPoint where zBelongsToTrackSegment=?', (tracksegment_pk,))
    for (i, ) in cur.fetchall():
        deltrackpoint(cur, i)
    logging.debug("Deleting tracksegment %i" % (tracksegment_pk,))
    if doit: cur.execute('delete from zCDTrackSegment where z_pk=?', (tracksegment_pk,))

def deltrack(cur, track_pk):
    if track_pk is None:
        logging.debug("Skipping track deletion - no track")
        return
    logging.debug('Finding related tracksegments')
    cur.execute('select z_pk from zCDTrackSegment where zBelongsToTrack=?', (track_pk,))
    for (i, ) in cur.fetchall():
        deltracksegment(cur, i)
    logging.debug("Deleting track %i" % (track_pk,) )
    if doit: cur.execute('delete from zCDTrack where z_pk=?', (track_pk,))

def delhistoryitem(cur, treeitem):
    logging.debug("Deleting History Item %s (%i)" % (treeitem['zdisplayedname'],
                                                     treeitem['z_pk']))
    # delete associated tracks - recurse down
    cur.execute('select ztrack from zcdtreeitem where z_pk=?', (treeitem['z_pk'],))
    for (i, ) in cur.fetchall():
        deltrack(cur, i)
    # delete associated lap tree item entries
    cur.execute('select z_pk,zdisplayedname from zcdtreeitem where z_ent=? and zbelongstorun=?', (lapcode, treeitem['z_pk']))
    for lap in cur.fetchall():
        logging.debug("Deleting lap %s (%i)" % (lap['zdisplayedname'],
                                                lap['z_pk']))
        if doit: cur.execute('delete from zcdtreeitem where z_pk=?', (lap['z_pk'],))
    # delete associated multisport entry
    if treeitem['zmultisport']:
        logging.debug("Deleting multisport entry %i" % (treeitem['zmultisport'],))
        if doit: cur.execute('delete from zcdtreeitem where z_pk=?', (treeitem['zmultisport'],)) 
    # delete the actual history item
    if doit: cur.execute('delete from zcdtreeitem where z_pk=?', (treeitem['z_pk'],))

# Find items with no track
logging.info("Deleting history tree items with no associated track... ")
cur.execute('select z_pk, zdisplayedname, zmultisport from zcdtreeitem where z_ent=? and ztrack is null', (historycode,))
counter = 0
for row in cur.fetchall():
    delhistoryitem(cur, row)
    counter += 1
logging.info("%i items deleted" % (counter,))

# Find duplicate items
logging.info('Deleting duplicates')
cur.execute('select distinct b.z_pk as z_pk, b.zDisplayedName as zdisplayedname, b.zmultisport as zmultisport from zcdtreeitem as a join zcdtreeitem as b on a.zdisplayedname=b.zdisplayedname where a.z_ent=:1 and b.z_ent=:1 and a.z_pk < b.z_pk', (historycode,))
counter = 0
for row in cur.fetchall():
    delhistoryitem(cur, row)
    counter += 1
logging.info('%i items deleted' % (counter,))

logging.info("Comitting...")
if doit: conn.commit()
logging.info("Done.")

# TODO: Find unconnected items:
# unconnected lap entries:
# select * from zcdtreeitem where zimagename = "lap" and zbelongstorun not in (select z_pk from zcdtreeitem)
# unconnected trackpoints:
# select from zcdtrackpoints where zcdtrack where
# 
# unconnected tracksegments:
# unconnected tracks
# unconnected multisport items/empty multisport items
