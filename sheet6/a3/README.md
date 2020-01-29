#   Game Labrys (Aufgabe 3)

##  Laden Sie sich das Spiel “Labrys” aus dem StudOn herunter. Für Hinweise zur Installation und Steuerung des Spiels lesen Sie bitte die README.txt. Neue Level können Sie mit einem Text-Editor erstellen, bspw. indem Sie die Datei ./level5/labyrinth editieren. Alle folgenden Aufgaben können Sie wahlweise mit labrys.32 oder labrys.64 lösen.

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

### a) Wallhack: Modifizieren Sie das Spiel, so dass Sie horizontal durch Wände laufen können ohne dabei herunterzufallen. Tipp: Verändern Sie die Methode(n) collide.

The executable `labrys.64.wallhack` contains the game with a wallhack. This was achieved by forcing the return value of the function `_ZN4Wall7collideEPfi` to be always `0x00`, so collisions with walls are never detected and the player can walk through them freely.

### b) Flyhack: Modifizieren Sie das Spiel, so dass Sie fliegen können. Tipp: Verändern Sie die Methode gravity.

### c) Speedhack: Modifizieren Sie das Spiel, so dass Sie schneller werden. Tipp: Verändern Sie den Multiplikator in step_forward oder save_state.

##  3. Exploitation: Sie verteilen selbst erstellte Levels um Ihre Mitspieler zu exploiten.

### a) Shellcode Injection: Gestalten Sie Level 5 derart, dass Schadcode auf dem Stack des Spielers ausgeführt wird. Beachten Sie, dass ASLR eingeschaltet und NX ausgeschaltet sind. Tipp: Verwenden Sie zur Demonstration den Shellcode von den Folien oder beliebigen Shellcode aus dem Internet, um /bin/sh auszuführen.

### b) Return Oriented Programming: Verwenden Sie nun die labrys_rop.{32,64} Binaries und beachten Sie, dass diese mit NX-Unterstützung kompiliert sind, d.h. starten Sie beliebigen Schadcode ohne ausführbaren Stack. Tipp: Tools wie github.com/JonathanSalwan/ROPgadget und github.com/sashs/Ropper unterstützen Sie bei der Suche nach Gadgets.