#!/usr/bin/env gnuplot

set xlabel 'Runs' # TODO: This should be a date
set ylabel 'Pace'

data="<./distances.sh 5000"
smoothed="<./distances.sh 5000 | awk '{print $1, (($3/60)/($2/1000))}' | ./ewma "
set terminal postscript eps
set output 'fivek.eps'
set yrange [4:7]

plot data using 1:(($3/60)/($2/1000)) title 'Raw',\
     smoothed using 1:2 with lines title 'Smoothed',\
     6 title 'High limit'