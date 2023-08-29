# Datei, die kompiliert werden soll (ohne Endung)
BINARY := oscillation_sensor
HEADER := cvc_numerics


# Flags
FLAGS := -lm -lgsl -lgslcblas -Wall -std=c99


# Kompilieren
$(BINARY): $(BINARY).o ../../$(HEADER).o
	gcc $(BINARY).o ../../$(HEADER).o -o $(BINARY) $(FLAGS)

$(BINARY).o: $(BINARY).c
	gcc -c $(BINARY).c

$(HEADER).o: ../../$(HEADER).c
	gcc -c ../../$(HEADER).c


# Ausführen
run: $(BINARY)
	./$< $(ARGS)


animate:
	manim -pqh --fps 60 $(BINARY)_animation.py $(BINARY)_scene


# Clean
clean:
	rm -f *.o
	rm -f $(HEADER).o
	rm -f *.exe
	rm -f $(BINARY)
	rm -f *.dat *.csv *.txt
	rm -f ../*.o
