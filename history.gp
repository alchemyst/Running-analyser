#!/usr/bin/env gnuplot

set xdata time
set format x "%h %Y"

weektarget = 10 # km
monthtarget = weektarget*4
yeartarget = weektarget*365.0/7

set terminal postscript eps


set timefmt "%Y-%m-%d"

set output "daily.eps"
set grid
set ylabel "Total distance / km"
plot "daily.dat" using 1:($3/1000) with lines smooth cumulative notitle

set ylabel "Distance / km"
set output "weekly.eps"
plot "weekly.dat" using 3:($4/1000) with impulses title "Weekly", \
     weektarget title "Target"

set output "monthly.eps"
set timefmt "%Y %m"
plot "monthly.dat" using 1:($4/1000) with impulses title "Monthly", \
     "" using 1:($4/1000) notitle with points ls 2, \
     monthtarget title "Target"

set output "yearly.eps"
set timefmt "%Y"
set format x "%Y"
plot "yearly.dat" using 1:($3/1000) with impulses title "Yearly", \
     "" using 1:($3/1000) notitle with points ls 2, \
     yeartarget title "Target"
