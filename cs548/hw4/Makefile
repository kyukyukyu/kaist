CC=gcc
CFLAGS=-c -Wall -lrt
LDFLAGS=
KECCAK_PACK=generic64_libkeccak.a.tar.gz
KECCAK_DIR=keccak
KECCAK_SRCDIR=$(KECCAK_DIR)/generic64/libkeccak.a
KECCAK_SOURCES=$(subst generic64/libkeccak.a/,$(KECCAK_DIR)/, \
	$(filter %.c, \
		$(filter-out %/, \
			$(shell tar tzf $(KECCAK_PACK)))))
SOURCES=main.c $(KECCAK_SOURCES)
OBJECTS=$(patsubst %.c,%.o,$(SOURCES))
EXECUTABLE=main

all: $(KECCAK_DIR) $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

$(KECCAK_DIR):
	mkdir -p $(KECCAK_DIR)
	tar xzf $(KECCAK_PACK) -C $(KECCAK_DIR)/
	mv $(KECCAK_SRCDIR)/* $(KECCAK_DIR)/

.c.o:
	$(CC) $(CFLAGS) $< -o $@

.PHONY: clean

clean:
	rm -f $(OBJECTS)
	rm -rf $(KECCAK_DIR)
