#!/bin/sh

awk '$1=='$1' {print substr(FILENAME, 13, 4), $1, $2}' bests/track* 
#|\
#while read a b c; do
#    echo `sed -n ${a}p history.dat` $b $c
#done