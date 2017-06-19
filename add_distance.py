#!/usr/bin/env python

import lxml.etree as ET
import argparse
import sys
import geopy.distance

NS = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'

def add_ns(string):
    return string.replace('NS', NS)

TRACKPOINTS = add_ns('.//NSTrackpoint')
DISTANCEMETERS = add_ns('.//NSTrackpoint/NSDistanceMeters')

parser = argparse.ArgumentParser("Add cumulative distance")
parser.add_argument("filenames", nargs="+")

args = parser.parse_args()

for filename in args.filenames:
    tree = ET.parse(filename)
    root = tree.getroot()

    # Figure out if we already have DistanceMeters
    d = len(root.findall(DISTANCEMETERS))
    if d > 0:
        continue

    cumulative_distance = 0
    oldpos = None
    for element in root.findall(TRACKPOINTS):
        lat = element.find(add_ns('NSPosition/NSLatitudeDegrees')).text
        lon = element.find(add_ns('NSPosition/NSLongitudeDegrees')).text
        pos = list(map(float, (lat, lon)))
        if oldpos is not None:
            cumulative_distance += geopy.distance.distance(oldpos, pos).meters
        oldpos = pos
        distance = ET.SubElement(element, add_ns('NSDistanceMeters'))
        distance.text = str(cumulative_distance)

    file_id = tree.find(add_ns('.//NSId')).text.replace(':', '-')
    outfile = '{}.xml'.format(file_id)

    print(filename, '->', outfile)

    tree.write(outfile, xml_declaration=True, encoding='UTF-8', standalone=False)
