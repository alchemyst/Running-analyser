#!/usr/bin/env python

# Based directly on disconnect.rb https://gist.github.com/1098861

import json
import mechanize
import os.path
import argparse
import getpass

LOGIN_PAGE = "https://connect.garmin.com/signin"
STEM = "http://connect.garmin.com/proxy/"
ACTIVITIES_SEARCH = STEM + "activity-search-service-1.0/json/activities?_dc=1220170621856&start=%i&limit=%i"
GPX_EXPORT = STEM + "activity-service-1.1/gpx/activity/%s?full=true"
KML_EXPORT = STEM + "activity-service-1.0/kml/activity/%s?full=true"
TCX_EXPORT = STEM + "activity-service-1.0/tcx/activity/%s?full=true"
TCXOUT = 'tcxnew/%s.tcx'

parser = argparse.ArgumentParser(description="Download activites from Garmin Connect")
parser.add_argument('username', nargs=1, help='Username on Garmin Connect')
parser.add_argument('--start', '-s', type=int, default=0,
                    help='Index of first activity to download (indexed backwards in time, so 0 is the last run)')
parser.add_argument('--limit', '-l', type=int, default=10,
                    help='Number of runs to download')


def login(br, username, password):
    # Login
    print "Logging in...",
    br.open(LOGIN_PAGE)
    br.select_form('login')
    br['login:loginUsernameField'] = username
    br['login:password'] = password
    br.submit()
    print "Done"


def findactivities(br, start, limit):
    print "Getting list of activities...",
    # Get list of activities
    search = json.loads(br.open(ACTIVITIES_SEARCH % (start, limit)).read())
    print "Done"
    return [item['activity']['activityId'] 
            for item in search['results']['activities']]


def download(activityId, br, targetdir):
    filename = os.path.join(targetdir, activityId + '.tcx')
    print "Downloading", activityId, '...',
    if os.path.exists(filename):
        print "File already exists"
    else:
        try:
            br.retrieve(TCX_EXPORT % activityId, filename)
            print "OK"
        except:
            print "Not OK"

if __name__ == "__main__":
    br = mechanize.Browser()
    args = parser.parse_args()
    username = args.username[0]
    password = getpass.getpass("Enter Garmin Connect password for " + username + ":")
    login(br, username, password)
    for activity in findactivities(br, args.start, args.limit):
        download(activity, br, 'tcxnew')
