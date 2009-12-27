#!/usr/bin/env gnuplot

set ticslevel 0
set view 34,300
set hidden3d
set terminal postscript eps
set output 'histogram.eps'

set xlabel "Run"
set ylabel "Speed (km/h)"
set zlabel "p"
#set yrange [4:15]

splot 'histogram.dat' using 1:2:3 with lines notitle

