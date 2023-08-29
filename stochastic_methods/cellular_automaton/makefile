# file names of the files to be complied
BINARY := cellular_automaton
HEADER1 := cvc_numerics
HEADER2 := cvc_rng


# flags
FLAGS := -lm -lgsl -lgslcblas -Wall -std=c99


# compile
$(BINARY): $(BINARY).o ../../$(HEADER1).o ../../$(HEADER2).o
	gcc $(BINARY).o ../../$(HEADER1).o ../../$(HEADER2).o -o $(BINARY) $(FLAGS)

$(BINARY).o: $(BINARY).c
	gcc -c $(BINARY).c

$(HEADER1).o: ../../$(HEADER1).c
	gcc -c ../../$(HEADER1).c

$(HEADER2).o: ../../$(HEADER2).c
	gcc -c ../../$(HEADER2).c


# run
run: $(BINARY)
	./$< $(ARGS)


# animate
animate:
	manim -pqh --fps 12 $(BINARY)_animation.py $(BINARY)_scene


# clean
clean:
	rm -f *.o
	rm -f ../../$(HEADER1).o
	rm -f ../../$(HEADER2).o
	rm -f *.exe
	rm -f $(BINARY)
	rm -f *.dat *.csv *.txt
	rm -f ../*.o