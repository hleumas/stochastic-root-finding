all: linearTest0.01.eps
cleanall: clean-all

clean-all: clean
	rm -f *.eps
clean:

%.eps: include asymptotika
	gnuplot asymptotika
.PHONY: clean-all cleanall clean all
FORCE:
