outputs=bestoverdistance.pdf histogram.pdf yearly.pdf monthly.pdf weekly.pdf daily.pdf fourk.pdf paceoverdist.pdf pcolor.png distancehistogram.pdf
input=Training\ Center.gtc
#input=ruanne.gtc
timefmt="%Y-%m-%d"

all: $(outputs)
	cp $(outputs) ~/Dropbox/training

%.pdf: %.eps
	epstopdf $<

fourk.eps paceoverdist.eps: distances.gp bests/track*
	./distances.gp

pcolor.png: allruns.csv pcolor.gp
	./pcolor.gp

bestoverdistance.eps: bestoverdistance.dat lastrun.dat bestoverdistance.gp 
	./bestoverdistance.gp

histogram.eps: allruns.csv histogram.gp
	./histogram.gp

distancehistogram.eps: distancehistogram.dat distancehistogram.gp
	./distancehistogram.gp

daily.eps monthly.eps weekly.eps yearly.eps: $(input) history.gp daily.dat weekly.dat monthly.dat yearly.dat
	./history.gp

daily.dat weekly.dat monthly.dat yearly.dat distancehistogram.dat: $(input)

%.dat: %.sql
	sqlite3 -separator " " $(input) < $< > $@

daily.sql: timequery.sql.m4
	m4 -D groupfmt="%Y-%m-%d" -D timefmt=$(timefmt) $< > $@

weekly.sql: timequery.sql.m4
	m4 -D groupfmt="%Y-%W" -D timefmt=$(timefmt) $< > $@

monthly.sql: timequery.sql.m4
	m4 -D groupfmt="%Y-%m" -D timefmt=$(timefmt) $< > $@

yearly.sql: timequery.sql.m4
	m4 -D groupfmt="%Y" -D timefmt=$(timefmt) $< > $@

bestoverdistance.dat lastrun.dat: allruns.csv bestoverdistance.py watchdistances.dat records.dat
	./bestoverdistance.py

allruns.csv: $(input)
	./sanitize.py
	./extractruns.py "$<"
	touch lastupdate

clean:
	-rm $(outputs) *.eps

realclean: clean
	-rm allruns.csv bestoverdistance.dat lastrun.dat

.PHONY: clean realclean
