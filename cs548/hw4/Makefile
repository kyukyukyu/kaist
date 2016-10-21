CC=gcc
CFLAGS=-g -c -Wall
LDFLAGS=
KECCAK_PACK=generic64_libkeccak.a.tar.gz
KECCAK_DIR=keccak
KECCAK_SRCDIR=$(KECCAK_DIR)/generic64/libkeccak.a
KECCAK_SOURCES=$(wildcard $(KECCAK_DIR)/*.c)
SOURCES=main.c $(KECCAK_SOURCES)
OBJECTS=$(patsubst %.c,%.o,$(SOURCES))
EXECUTABLE=main

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

$(KECCAK_SOURCES): $(KECCAK_PACK)
	mkdir -p $(KECCAK_DIR)
	tar xzf $(KECCAK_PACK) -C $(KECCAK_DIR)/
	mv $(KECCAK_SRCDIR)/* $(KECCAK_DIR)/

.c.o:
	$(CC) $(CFLAGS) $< -o $@

.PHONY: clean

clean:
	rm -f $(OBJECTS)
	rm -rf $(KECCAK_DIR)
