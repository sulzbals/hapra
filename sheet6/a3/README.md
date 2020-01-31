#   Game Labrys (Aufgabe 3)

##  1. Cracking: Sie wollen für das Spiel nicht zahlen und entscheiden sich, es zu cracken.

### a) Keygen:

### i. Erstellen Sie einen gültigen Lizenzschlüssel für das Spiel.

A valid key is `IKYIS-XXMMM-FKVVB-76D1U-XYSRX`.

### ii. Schreiben Sie einen Key-Generator, der mehrere Schlüssel generiert.

You can use `python3 key-gen.py -n [NUMBER_OF_KEYS]` to generate a number of random keys. Further details are documented into the script.

### b) Patch: Modifizeren Sie das Spiel, so dass es auch ohne Lizenz startet.

The executable `labrys.64.cracked` works without a `license.key` file. I managed to do it by overwriting the beginning of the routine that is run when `fopen` fails with a jump to an address after the validation routine. Notice that the game will only work when the key file either does not exist or has a valid key, so if the file exists and does not contain a valid key, the game will not run.

A `SEGMENTATION FAULT` happens when the game is closed, but the functionality of the game is not affected by the crack.

##  2. Cheating: Sie verschaffen sich Vorteile gegenüber Mitspielern indem Sie cheaten.

### a) Wallhack: Modifizieren Sie das Spiel, so dass Sie horizontal durch Wände laufen können ohne dabei herunterzufallen.

The executable `labrys.64.wallhack` contains the game with a wallhack. This was achieved by forcing the return value of the function `_ZN4Wall7collideEPfi` to be always `0x00`, so collisions with walls are never detected and the player can walk through them freely.

### b) Flyhack: Modifizieren Sie das Spiel, so dass Sie fliegen können.

The executable `labrys.64.flyhack` contains the game with a flyhack. This was achieved by changing an instruction of the function `_ZN6Player10save_stateEv` so that the variable `flying` is always set to `0x01` independently of the value of `spellEagle`, so the player can fly all the time.

### c) Speedhack: Modifizieren Sie das Spiel, so dass Sie schneller werden. Tipp: Verändern Sie den Multiplikator in step_forward oder save_state.

The executable `labrys.64.speedhack` contains the game with a speedhack. This was achieved by changing an instruction of the function `_ZN6Player10save_stateEv` so that the variable `moveSpeed` is always set to `DAT_0003af88` (the higher speed) independently of the value of `spellHorse`, so the player's speed is always high.

##  3. Exploitation: Sie verteilen selbst erstellte Levels um Ihre Mitspieler zu exploiten.

### a) Shellcode Injection: Gestalten Sie Level 5 derart, dass Schadcode auf dem Stack des Spielers ausgeführt wird. Beachten Sie, dass ASLR eingeschaltet und NX ausgeschaltet sind.

The exploit consists of two parts:

1. An one-lined string stored on `level5/labyrinth` that is big enough to overflow the buffer allocated on the stack and overwrite the return address;
2. An environment variable containing the shellcode to be run, preceeded by a "NOP sled" to increase the size of the code and therefore the probability of it being executed.

In order to perform the first part of the exploit, I used the `cyclic` method from `pwntools` to generate a large sequence (to cause a buffer overflow) and saved it to `level5/labyrinth`. Then I ran the game in `gdb` and found out which part of the sequence was loaded into the `EIP` ("raaf"). Finally I used the `cyclic_find` method to retrieve the part of the sequence that would overwrite the stack just until the position before the return address, concatenated it to a given address, and saved that to the labyrinth file. By doing this, the program flow is always redirected to that address when level 5 is selected.

Now that we control the instruction pointer, we have to inject the shellcode and point to it. Since `ASLR` is enabled, the best we can do is having a good guess of where this code will be loaded to. That is why NOP sleding is used, so if the flow is redirected to any of the NOPs that were injected, the shellcode is executed as well. The shellcraft is injected by setting an environment variable (which is loaded to the stack) containing it.

In order to perform the exploit, run `python3 shellcode-inject.py`. It will write a payload into `level5/labyrinth` that redirects the flow to the address `0xffa41fb8` and also will write the shellcraft to `shellcode.32`. Both files are included with the solution as well. If you keep running `SHELLCODE=$(cat shellcode.32) ./labrys.32`, eventually `0xffa41fb8` will point to some part of the shellcraft, and a shell will be spawned if you select level 5.

### b) Return Oriented Programming: Verwenden Sie nun die labrys_rop.{32,64} Binaries und beachten Sie, dass diese mit NX-Unterstützung kompiliert sind, d.h. starten Sie beliebigen Schadcode ohne ausführbaren Stack.

For this challenge, I used the `Ropper` tool to generate a rop chain for the `labrys_rop.64` executable (more specifically `ropper --file labrys_rop.64 --chain "execve cmd=/bin/sh"`), and changed it slightly in order to perform the exploit. The changes consist mostly of using the same `cyclic` method from the previous exercise to generate the padding inserted before the rop chain (for the 64 bit version it must be until "vaaf" instead) and writing the result to `level5/labyrinth` instead of printing it. After running `python3 rop-chain.py` to generate the labyrinth file, you can perform the exploit by running `./labrys_rop.64` and selecting level 5 to spawn a shell.