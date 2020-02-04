#   Obfuscated Binaries (Aufgabe 4)

##  1. Beschreiben Sie mit welchen Techniken sich die Programme schützen.

### Static Analysis Protection

* Two strings are stored encoded in the `.data` section. After analysing the program, I was able to understand how they are decoded, and wrote a `gdb` command to easily decode any of those during a debugging session. It can be found on `hapra-decode.py`.

* The program has a lot of junk code. There are useless instructions like jumps that point to the next instruction and also several occurences of instructions that copy the contents of a register to the same register.

* All the functions (including `main`) are merged into the `.text` section. There are no labels.

### Dynamic Analysis Protection

* Apparently the program defines a signal handler for signal `SIGUSR1`, and when the code is debugged with `gdb`, sometimes this signal is thrown to its own process using the function `raise`, changing the program's behavior.

* When debugging, different routines are run to mislead the user, and often a success message is printed even though the password is incorrect.

##  2. Wo findet die Überprüfung des Passworts statt? Wie lautet das Lösungswort?

The password is one of the encoded strings (the other one is the real success message that is printed when the correct password is given). It can be decoded with my custom command. The process is described below:

1. Open `obfusticated.32` on `gdb`;
2. Run `source hapra-decode.py` to load the command;
3. Decode the string with the password with `hapra-decode (char *) 0x804a02c`. It should be `I am a H4Xx0r!`.

Therefore, the challenge can be solved by running `./obfusticated.32 "I am a H4Xx0r!"`.