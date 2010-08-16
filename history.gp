#!/usr/bin env gnuplot

set timefmt "%Y %m"
set xdata time
set format x "%h %Y"

set terminal postscript 
set output "monthly.eps"
plot '<sqlite3 -separator " " history.sqlite "select * from permonth"' using 1:3 with boxes title "Monthly" 

set timefmt "%Y %j"
set output "weekly.eps"
plot '<sqlite3 -separator " " history.sqlite "select year, week*7+1 from perweek"' using 1:3 with boxes title "Weekly totals"
