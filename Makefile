outputs=bestoverdistance.pdf histogram.pdf pcolor.png
input=Training\ Center.gtc
#input=ruanne.gtc

all: ${outputs}

%.pdf: %.eps
	epstopdf $<

pcolor.png: allruns.csv pcolor.gp
	./pcolor.gp

bestoverdistance.eps: bestoverdistance.dat lastrun.dat bestoverdistance.gp 
	./bestoverdistance.gp

histogram.eps: allruns.csv histogram.gp
	./histogram.gp

bestoverdistance.dat lastrun.dat: allruns.csv bestoverdistance.py watchdistances.dat records.dat
	./bestoverdistance.py

allruns.csv: $(input)
	./extractruns.py "$<"

clean:
	-rm ${outputs} *.eps

realclean: clean
	-rm allruns.csv bestoverdistance.dat lastrun.dat

.PHONY: clean realclean