# file names of the files to be complied
BINARY := nonlinear_map
HEADER := cvc_numerics


# flags
FLAGS := -lm -lgsl -lgslcblas -Wall -std=c99


# compile
$(BINARY): $(BINARY).o ../../$(HEADER).o
	gcc $(BINARY).o ../../$(HEADER).o -o $(BINARY) $(FLAGS)

$(BINARY).o: $(BINARY).c
	gcc -c $(BINARY).c

$(HEADER).o: ../../$(HEADER).c
	gcc -c ../../$(HEADER).c


# run
run: $(BINARY)
	./$< $(ARGS)


# plot
plot:
	python3.12 $(BINARY)_plotting.py


# animate
animate:
	manim -pqh --fps 60 $(BINARY)_animation.py $(BINARY)_scene


# clean
clean:
	rm -f *.o
	rm -f ../../$(HEADER).o
	rm -f *.exe
	rm -f $(BINARY)
	rm -f *.dat *.csv *.txt
	rm -f ../*.o