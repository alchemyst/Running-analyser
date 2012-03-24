#!/bin/sh

awk '$1=='$1' {print substr(FILENAME, 13, 4), $1, $2}' bests/track* |\
while read a b c; do
    n=`echo $a | sed 's/^0*//'`
    echo `sed -n "/^${n} /p" history.dat` $b $c
done