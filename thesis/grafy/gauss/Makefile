all: newton_big.eps
cleanall: clean-all

clean-all: clean
	rm -f *.eps
clean:

%.eps: include gauss
	gnuplot gauss
.PHONY: clean-all cleanall clean all
FORCE:
