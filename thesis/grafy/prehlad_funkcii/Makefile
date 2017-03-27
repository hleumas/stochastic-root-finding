all: linear.eps
cleanall: clean-all

clean-all: clean
	rm -f *.eps
clean:

%.eps: include prehlad
	gnuplot prehlad
.PHONY: clean-all cleanall clean all
FORCE:
