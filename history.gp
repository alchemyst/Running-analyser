#!/usr/bin/env gnuplot

set timefmt "%Y %m"
set xdata time
set format x "%h %Y"

set terminal postscript eps
set output "monthly.eps"
plot '<sqlite3 -separator " " Training\ Center.gtc < monthly.sql' using 1:($3/1000) with impulses title "Monthly" 

set timefmt "%Y %j"
set output "weekly.eps"
plot '<sqlite3 -separator " " Training\ Center.gtc < weekly.sql | awk ''{print $1, $2*7+1, $3}''' using 1:($3/1000) with impulses title "Weekly"
