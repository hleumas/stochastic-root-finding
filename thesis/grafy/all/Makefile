all: cauchy.eps
cleanall: clean-all

clean-all: clean
	rm -f *.eps
clean:

%.eps: include vsetky
	gnuplot vsetky
.PHONY: clean-all cleanall clean all
FORCE:
