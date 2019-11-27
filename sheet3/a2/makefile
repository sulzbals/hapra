CC=				gcc
LFLAGS=			-shared -fPIC -ldl

.PHONY:			default clean purge

default:		test

test:			test.c sandbox.so
				$(CC) $< -o $@

sandbox.so:		sandbox.c
				$(CC) $^ -o $@ $(LFLAGS)

clean:
				@rm -f test

purge:			clean
				@rm -f sandbox.so