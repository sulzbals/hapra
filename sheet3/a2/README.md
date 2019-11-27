#   LD_PRELOAD-based sandbox

##  Library

### Description

The library defines two functions named `read` and `write`. Since it is pre-loaded, its symbols will be written to the symbol table BEFORE the standard `libc`'s symbols. This means that all `read` and `write` calls of the program being run will execute our library's routines, instead of the standard ones.

Both `read` and `write` run a routine that verifies if the file being read/written is whitelisted. If yes, the dynamic linker is used to retrieve the standard `libc` symbol for `read` or `write`, and this function is called with the same parameters as our library's call. If not, the function returns `NULL`.

### Usage

To compile the sandboxing library only:

`make sandbox.so`

To sandbox a given program `example_program`:

`LD_PRELOAD=$PWD/sandbox.so ./example_program`

##  Test routine

### Description

The test consists of a C program and a bash script. The C program tests the `read` and `write` calls for a given file. The script is a wrapper that generates an environment with a whitelisted and a non-whitelisted file, then runs the sandboxed binary program for both files.

### Usage

To test the library first compile it and the test binary:

`make`

Then run the test script:

`./test.sh`

### Output

The routine should succeed to `read` from and `write` to the whitelisted file, and be unable to do the same for the non-whitelisted file.

##  Insecurities

This sandbox can be easily bypassed by:

1. Using the actual system calls for read/write operations instead of the `libc` wrappers;

2. Using only static linking so the whole symbol table and definitions intended to be used by the program are tied to the executable.