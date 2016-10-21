CC=gcc
# Assuming x86_64 which is little endian.
CFLAGS=-g -c -Wall -DUSER_LITTLE_ENDIAN
LDFLAGS=
SOURCES=main.c $(wildcard sha256/*.c lsh/src/*.c)
OBJECTS=$(patsubst %.c,%.o,$(SOURCES))
EXECUTABLE=main

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@

.PHONY: clean

clean:
	rm -f $(OBJECTS)
