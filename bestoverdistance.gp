#!/usr/bin/env gnuplot

set ylabel 'Speed / km/h'
set xlabel 'Distance / km'
set y2label 'Pace / min/km'
set grid

set terminal postscript eps
set output 'bestoverdistance.eps'
#set terminal png enhanced
#set output 'bestoverdistance.png'

# 10 6
# 12 5
# 14 4.28571
# 15 4
# 16 3.75
# 18 3.33333
# 20 3
# 22 2.72727
# 23 2.6087
# 24 2.5
# 25 2.4
# 26 2.30769
# 27 2.22222
# 28 2.14286
# 29 2.06897
# 30 2

set y2tics nomirror ("6:00" 10, "5:00" 12, "4:29" 14, "4:00" 15, "3:45" 16, "3:30" 18, "3:00" 20, "2:30" 24, "2:00" 30, "1:40" 36, "1:30" 40)

set log x
#set log y

set xrange [.1:100]
set yrange [8:40]
#set y2range [8:40]

set style data lines
#set key center top

recordfactor=0.631 # 20 minute 5 km - target
bestfile = 'bestoverdistance.dat'
lastfile = 'lastrun.dat'
records = 'records.dat'

# fit function for records
a = 8.02651     
b = 2.70985     
c = 2.64571e-06 
d = 42.8487     
e = 0.0773884   
f = 0.331192    
ff(x) = a + b*exp(-c*(x-d)**2) - e*x**f

kph(mps) = (mps)*3600/1000

recordcurve(x) = kph(ff(x*1000))

# fit [0:100000] ff(x) records using 1:($1/$2) via a, b, c, d, e, f

plot bestfile using ($1/1000):(kph($1/$2))  title 'Best Ever',\
     lastfile using ($1/1000):(kph($1/$2))  title 'Last Run',\
     records using ($1/1000):(kph($1/$2)) with points title "Actual world records (men)",\
     "" using ($1/1000):(kph($1/$3)) with points title "Actual world records (women)",\
     recordcurve(x) notitle,\
     0.9*recordcurve(x) notitle,\
     0.631*recordcurve(x) title '20 minute 5 km (0.63 record)',\
     0.5855*recordcurve(x) title '1:40 half-marathon (0.59 record)'


