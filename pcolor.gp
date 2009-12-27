#!/usr/bin/env gnuplot

set xlabel "Run"
set ylabel "Speed (km/h)"

set pm3d map interpolate 10,1
set terminal png crop
set output 'pcolor.png'
splot 'histogram.dat' using 1:2:3 notitle 
