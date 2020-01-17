#   Basic Reverse Engineering (Aufgabe 1)

##  • Wie lautet das Passwort für Challenge 1?

The password for this challenge is `p4ssw0rd`. I found it out using the following method:

1. Open the program in `gdb`;

2. Disassemble the routine that verify the password for the challenged (`disass checkEasy`);

3. Notice that the verification consists of loading the provided input and the address `0x400940` into the parameter registers, then calling `strcmp`;

4. Interpret the address as a pointer to `char` in order to retrieve the password string (`p (char *) 0x400940`).

##  • Wie lautet das Passwort für Challenge 2?

The password for this challenge is `1337`. I found it out using the following method:

1. Open the program in `gdb`;

2. Disassemble the routine that verify the password for the challenged (`disass checkMedium`);

3. Notice that the verification consists of loading the provided input and the password string into the parameter registers, then calling `strcmp`;

4. Defined a breakpoint at the instruction that call `strcmp` (`b *0x00000000004006aa`);

5. Run the program (`r test`). It will stop at the breakpoint;

6. Interpret the address on the parameter register as a pointer to `char` in order to retrieve the password string (`p (char *) $rsi`).

##  • Wie lautet das Passwort für Challenge 3?

The password for this challenge is `zyvgjqpc`. I found it out using the same method as the previous challenge.