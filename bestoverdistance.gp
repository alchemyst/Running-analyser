#!/usr/bin/env gnuplot

set ylabel 'Speed / km/h'
set xlabel 'Distance / km'
set y2label 'Pace / min/km'
set grid

set terminal postscript eps
set output 'bestoverdistance.eps'

# 10 6
# 12 5
# 14 4.28571
# 15 4
# 16 3.75
# 18 3.33333
# 20 3
# 22 2.72727
# 23 2.6087
# 24 2.5
# 25 2.4
# 26 2.30769
# 27 2.22222
# 28 2.14286
# 29 2.06897
# 30 2

set y2tics nomirror ("6:00" 10, "5:00" 12, "4:29" 14, "4:00" 15, "3:45" 16, "3:30" 18, "3:00" 20, "2:30" 24, "2:00" 30)
set logscale x

set xrange [.1:20]
set yrange [8:30]
set y2range [8:30]

set style data lines
#set key center top

recordfactor=0.531
bestfile = 'bestoverdistance.dat'
lastfile = 'lastrun.dat'
records = 'records.dat'

#     bestfile using ($1/1000):($2/60/$1*1000) axis x1y2  title 'Pace',\

plot bestfile using ($1/1000):(($1/$2)*3600/1000)  title 'Best Ever',\
     lastfile using ($1/1000):(($1/$2)*3600/1000)  title 'Last Run',\
     records using ($1/1000):(recordfactor*$1/$2*3600/1000)  title sprintf('%i%% of world record speeds', recordfactor*100)
