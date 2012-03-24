#!/usr/bin/env gnuplot

set timefmt "%Y %m"
set xdata time
set format x "%h %Y"

weektarget = 10 # km
monthtarget = weektarget*4

set terminal postscript eps
set output "monthly.eps"
plot "monthly.dat" using 1:($3/1000) with impulses title "Monthly", \
     "" using 1:($3/1000) notitle with points ls 2, \
     monthtarget title "Target"

set timefmt "%Y %j"
set output "weekly.eps"
plot "weekly.dat" using 1:($3/1000) with impulses title "Weekly", \
     weektarget title "Target"
