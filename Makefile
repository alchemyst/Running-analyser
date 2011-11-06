outputs=bestoverdistance.pdf histogram.pdf monthly.pdf weekly.pdf fivek.pdf pcolor.png
input=Training\ Center.gtc
#input=ruanne.gtc

all: $(outputs)
	cp $(outputs) ~/Dropbox/training

%.pdf: %.eps
	epstopdf $<

fivek.eps: distances.gp
	./distances.gp

pcolor.png: allruns.csv pcolor.gp
	./pcolor.gp

bestoverdistance.eps: bestoverdistance.dat lastrun.dat bestoverdistance.gp 
	./bestoverdistance.gp

histogram.eps: allruns.csv histogram.gp
	./histogram.gp

monthly.eps weekly.eps: $(input) history.gp weekly.sql monthly.sql
	./history.gp

weekly.sql: timequery.sql.m4
	m4 -D timefmt="%Y %W" timequery.sql.m4 > $@

monthly.sql: timequery.sql.m4
	m4 -D timefmt="%Y %m" timequery.sql.m4 > $@

bestoverdistance.dat lastrun.dat: allruns.csv bestoverdistance.py watchdistances.dat records.dat
	./bestoverdistance.py

allruns.csv: $(input)
	./sanitize.py
	./extractruns.py "$<"

clean:
	-rm $(outputs) *.eps

realclean: clean
	-rm allruns.csv bestoverdistance.dat lastrun.dat

.PHONY: clean realclean
