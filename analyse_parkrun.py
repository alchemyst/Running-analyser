#!/usr/bin/env python

import pandas
import sys
import matplotlib.pylab as plt
import bs4
import argparse
import sys

parser = argparse.ArgumentParser(description='Analyse parkrun html')
parser.add_argument('filename', type=argparse.FileType('r'),
                    help='The filename to be parsed')
parser.add_argument('--plot', default=False, action='store_true',
                    help='Plot results')
parser.add_argument('--csv', default=False, action='store_true',
                    help='Write csv')
parser.add_argument('--output', default=sys.stdout, type=argparse.FileType('w'),
                    help='Write parsed data to CSV')
args = parser.parse_args()


## This would work if the parsing worked

# d, = pandas.read_html(filename)
# d.dropna(axis=1, how='all', inplace=True)
names = ['pos', 'parkrunner', 'time', 'agecat', 'agegrade', 'gender', 'genderpos', 'club', 'note', 'totruns']
# d.columns = names

# # Currently, the time column is not parsed correctly.
# d.Time = d.Time.apply(lambda x: 60*x.hour + x.minute if not pandas.isnull(x) else pandas.np.nan)

## So, we parse directly

nan = pandas.np.nan

def seconds(timestr):
    try:
        parts = timestr.split(':')
        s = 0
        for i, part in enumerate(reversed(parts)):
            s += int(part)*60**i
        return s
    except:
        return nan

def tryint(timestr):
    try:
        return int(timestr)
    except:
        return nan

    
def parserow(tr):
    tds = tr.findAll('td')
    pos, parkrunner, time, agecat, agegrade, gender, genderpos, club, note, totruns, _ = [td.text for td in tds]

    return [tryint(pos), parkrunner, seconds(time), agecat, agegrade[:-3], gender, tryint(genderpos), club, note, tryint(totruns)]
    
table = bs4.BeautifulSoup(args.filename.read()).table.findAll('tr')
d = pandas.DataFrame([parserow(tr) for tr in table if len(tr.findAll('td')) > 0], columns=names)

def sandrocks(d):
    return d[d.parkrunner.str.contains('SANDROCK')]


def plot(d, gender, posfield):
    if gender:
        subset = d[d.gender==gender]
    else:
        subset = d
    highlight = sandrocks(subset)
    plt.plot(subset.time, subset[posfield])
    plt.plot(highlight.time, highlight[posfield], 'ro')


if args.plot:
    for gender, posfield in [[None, 'pos'],
                             ['M', 'genderpos'],
                             ['F', 'genderpos']]:
        plot(d, gender, posfield)
    plt.ylabel('Number of runners')
    plt.xlabel('Time / m')
    plt.show()

if args.csv:
    d.to_csv(args.output)
