#!/usr/bin/env gnuplot

data="<./distances.sh 4000"
smoothed="<./distances.sh 4000 | awk '{print $2, (($5/60)/($4/1000))}' | ./ewma "

kph(speed, distance) = (speed/distance)*3600/1000

set terminal postscript eps
set output 'paceoverdist.eps'

set ylabel 'Speed / km/h'
set xlabel 'Total activity length /  km'
set y2label 'Pace / min/km'
set grid
set y2tics nomirror ("7:00" 8.57, "6:30" 9.23,"6:00" 10, "5:00" 12, "4:29" 14, "4:00" 15, "3:45" 16, "3:30" 18, "3:00" 20, "2:30" 24, "2:00" 30)
set xrange [5:]
set yrange [8:]

plot data using ($3/1000):(kph($4,$5)) title 'Best 5k',\
     'bestoverdistance.dat' using ($1/1000):(kph($1,$2)) with lines title 'Best over this distance'

#-----------
set output 'fourk.eps'

set xlabel 'Date'
set ylabel 'Pace'
unset y2label
set xdata time
set timefmt "%Y-%m-%d"
set grid x
#set format x "%Y %m"
set yrange [4.5:8]
set autoscale x
set xrange ["2011-01-01":]

plot data using 2:(($5/60)/($4/1000)) title 'Raw',\
     smoothed using 1:2 with lines title 'Smoothed',\
     6 title 'High limit'
