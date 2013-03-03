#!/usr/bin/env gnuplot

set term postscript eps
set output 'distancehistogram.eps'

set xlabel 'Distance / km'
set ylabel 'Number of runs below this distance'
set grid

plot 'distancehistogram.dat' using ($1/1000):0 with lines notitle

