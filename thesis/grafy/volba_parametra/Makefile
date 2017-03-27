all: newton_linear.eps
cleanall: clean-all

clean-all: clean
	rm -f *.eps
clean:

%.eps: include parameter
	gnuplot parameter
.PHONY: clean-all cleanall clean all
FORCE:
