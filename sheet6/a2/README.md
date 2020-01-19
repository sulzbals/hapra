#   Basic Exploitation (Aufgabe 2)

##  1. Bringen Sie beide Programme mit einer langen Eingabe zum Absturz.

`./hack-me.32 $(python -c 'print "A" * 0x110')`

`./hack-me.64 $(python -c 'print "A" * 0x120')`

##  2. Erklären Sie, wie es zum Absturz der Programme kommt. Welche Anweisung ist fehlerhaft und was passiert mit dem Return address ? Zeichnen Sie den Stack vor und nach dieser Anweisung als ASCII-Art.

By analyzing the behavior of both executables with `gdb`, it can be concluded that the string passed as argument to the program is passed by reference to the function `normal`, which allocates a buffer in the stack and copies the string to it with `strcpy`.

Since no bound checking is performed, we can exploit the program with a stack overflow simply by passing a string larger than the size of the buffer it is copied to. The detailed approaches for each architecture is described below:

### IA32

Given the disassembled code of the executable and that its architecture consists of 32-bit (4 bytes) words, the state of the stack can be expressed, at the moment `strcpy` is called, as follows:

<pre>
              | ........... |
              |  Saved EIP  | < Return address
   0x0(%ebp): |  Saved EBP  | < EBP (Base pointer)
  -0x4(%ebp): | ?? ?? ?? ?? |
              | ........... |
              | ........... |
-0x104(%ebp): | ?? ?? ?? ?? |
-0x108(%ebp): | ?? ?? ?? ?? | < dest
              | ........... |
              | ........... |
-0x124(%ebp): | ?? ?? ?? ?? | < ESP (Stack pointer)
              |_____________|
</pre>

Where `dest` is the pointer passed as parameter to the `strcpy`, which points to the memory where the `src` string must be copied to.

By passing an argument that consists of the character `A` (`0x41` in ASCII) repeated `0x110` times, the `strcpy` call writes:

* The `0x108` bytes allocated for the buffer;
* The `0x4` bytes that held the previous stack frame's base pointer;
* The `0x4` bytes that held the instruction pointer related to the previous stack frame (return address).

<pre>
              | ........... |
              | 41 41 41 41 | < Return address
   0x0(%ebp): | 41 41 41 41 | < EBP (Base pointer)
  -0x4(%ebp): | 41 41 41 41 |
              | ........... |
              | ........... |
-0x104(%ebp): | 41 41 41 41 |
-0x108(%ebp): | 41 41 41 41 | < dest
              | ........... |
              | ........... |
-0x124(%ebp): | ?? ?? ?? ?? | < ESP (Stack pointer)
              |_____________|
</pre>

Since the base pointer and the instruction pointer were overwritten and now point to invalid addresses, the program crashes with a `SEGMENTATION FAULT`.

### AMD64

Given the disassembled code of the executable and that its architecture consists of 64-bit (8 bytes) words, the state of the stack can be expressed, at the moment `strcpy` is called, as follows:

<pre>
              | ....................... |
              |        Saved RIP        | < Return address
   0x0(%rbp): |        Saved RBP        | < RBP (Base pointer)
  -0x8(%rbp): | ?? ?? ?? ?? ?? ?? ?? ?? |
              | ....................... |
              | ....................... |
-0x118(%rbp): | ?? ?? ?? ?? ?? ?? ?? ?? |
-0x110(%rbp): | ?? ?? ?? ?? ?? ?? ?? ?? | < dest
              | ....................... |
              | ....................... |
-0x130(%rbp): | ?? ?? ?? ?? ?? ?? ?? ?? | < RSP (Stack pointer)
              |_________________________|
</pre>

Where `dest` is the pointer passed as parameter to the `strcpy`, which points to the memory where the `src` string must be copied to.

By passing an argument that consists of the character `A` (`0x41` in ASCII) repeated `0x120` times, the `strcpy` call writes:

* The `0x110` bytes allocated for the buffer;
* The `0x8` bytes that held the previous stack frame's base pointer;
* The `0x8` bytes that held the instruction pointer related to the previous stack frame (return address).

<pre>
              | ....................... |
              | 41 41 41 41 41 41 41 41 | < Return address
   0x0(%rbp): | 41 41 41 41 41 41 41 41 | < RBP (Base pointer)
  -0x8(%rbp): | 41 41 41 41 41 41 41 41 |
              | ....................... |
              | ....................... |
-0x118(%rbp): | 41 41 41 41 41 41 41 41 |
-0x110(%rbp): | 41 41 41 41 41 41 41 41 | < dest
              | ....................... |
              | ....................... |
-0x130(%rbp): | ?? ?? ?? ?? ?? ?? ?? ?? | < RSP (Stack pointer)
              |_________________________|
</pre>

Since the base pointer and the instruction pointer were overwritten and now point to invalid addresses, the program crashes with a `SEGMENTATION FAULT`.

##  3. Manipulieren Sie mit Ihrer Eingabe den Programmfluss von hack-me.32 so, dass die Funktion secret ausgeführt wird:

Given that the address of the function `secret` is `0x08048480` and the addresses are stored as little-endian, the simple python script from exercise 1 can be slightly altered to overwrite the return address and execute the secret function:

`./hack-me.32 $(python -c 'print "\x80\x84\x04\x08" * (0x110 / 4)')`

Notice that the same `0x110` bytes are written. Since the size of the string to be repeated is multiplied by 4 (`A` -> `\x80\x84\x04\x08`), it is repeated `0x110 / 4` times to obtain the same length. The last occurence of it overwrites the return address, then when the function `normal`'s stack frame is deallocated, the injected address is copied to the instruction pointer, then `secret` is executed.

##  4. Injizieren Sie einen ähnlichen Angriffsvektor in das Programm hack-me.64 um dort ebenfalls secret zur Ausführung zu bringen.

Given that the address of the function `secret` is `0x00000000004005e0` and the addresses are stored as little-endian, the simple python script from exercise 1 can be slightly altered to overwrite the return address and execute the secret function:

`./hack-me.64 $(python -c 'print "A" * (0x120 - 0x8) + "\xe0\x05\x40\x00\x00\x00\x00\x00"')`

This time, the approach of overflowing the stack with a string consisting of the address repeated multiple times does not work, because it contains null bytes. Therefore, `strcpy` would return after copying the 4th byte and no buffer overflow would ever occur. This can be avoided by using the old approach of writing `A` repeated multiple times, except for the last word, which would overwrite the return address (`0x120 - 0x8`). This particular word is replace by the address of `secret`, and that is how it ends up being executed.