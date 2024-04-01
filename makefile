CC = clang
CFLAGS = -std=c99 -Wall -pedantic

all: libphylib.so _phylib.so

libphylib.so: phylib.o 
	$(CC) -shared phylib.o -lm -o libphylib.so 

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -fPIC -c phylib_wrap.c -o phylib_wrap.o -I/usr/include/python3.11

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

clean:
	rm -f .o.so phylib_wrap.c