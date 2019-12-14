#   Flappy Hacks (Aufgabe 3)

##  1. Beschreiben Sie, wie sich das APK gegen Emulatoren schutzt.

### com/prosper/ts/hapra/GameActivity.a(String)

This method compares the given string with patterns that indicate the application is being run in emulator instead of a physical device. If it matches at least one of those patterns, the `finish()` routine is called and program finishes.

Bypass: I was able to prevent this routine from running by simply deleting it from the smali file.

### com/prosper/ts/hapra/GameActivity.b()

This method retrieves the battery charging level and calls `System.exit()` if it is 50%. I believe this might be a standard value for emulators and the app assumes it is being emulated if this is the charging level during startup.

Bypass: I was able to prevent this termination by deleting the instruction from the smali file that calls `System.exit`.

### com/prosper/ts/hapra/b/a.a(String)

This method is essentially identical to the first one described here (`com/prosper/ts/hapra/GameActivity.a(String)`).

Bypass: I used the same strategy from the first method.

### com/prosper/ts/hapra/b/b.b(String)

This method is also very similar to the first and previous one, except that it does not terminate the program, but returns `true` when one of the conditions is match. The return value is used by the program after calling this method to then decide if it terminates or not.

Bypass: I deleted most of the method's code from the smali file, letting only two instructions in order to always return `false`.

### com/prosper/ts/hapra/b/b.b()

This method checks the bluetooth adapter, terminating the problem if:

1. The adapter or the address of the adapter is `null` or
2. An exception is caught trying to access this the adpater.

The logic behind this verification is that a physical device should have a bluetooth adapter, so, if there is none, probably the app is being run in an emulator.

Bypass: I was able to prevent this termination by deleting both instructions (when the adapter-related values are `null` and when an exception is caught) from the smali file that calls `System.exit`.

Later in the same method, there is an if-statement that detects if the previous method described here was modified to always return `false` (exactly what I did). It consists of calling it with "fish" as parameter, then calling `System.exit()` if it returns `false`. It looks like "fish" would return `true` in a normal execution, so if someone modifies the verification routine in order to prevent the program from terminating, it is terminated anyway later on the code.

Bypass: I was able to prevent this termination by deleting the instruction from the smali file that calls `System.exit`.

##  2. Modifizieren Sie das APK, so dass es sich in einem Emulator ausfuhren lässt.

After performing all modifications described on the previous exercise, I repackaged the application. Then, I could play the game normally in an emulator by running this modified version (`flappyHacks_modified.apk`).

##  Reverse Engineering: Der Entwickler des Spiels hat Cheats in das Spiel eingebaut. Diese können vor dem Start eingegeben werden und müssen durch das APK verifiziert werden. Finden Sie den Mechanismus für die Verifikation heraus und beschreiben Sie diesen. Welche Cheats existieren?

The application has a hidden Java package on assets/gfx/game/Flappy.png. It is not a PNG file, just raw, encoded data. On com/prosper/ts/hapra/a.a it is possible to see how this package is acessed: It is decoded by `xor`ing the file byte by byte with the bytes of the string `HaPra`, resulting in a DEX file. This file contains the package `com.cheats.cheatengine`, which is used to verify if the user input is a valid cheat, and also contains routines to, for example, decode strings related to the cheat engine and print them in the screen.

I was able to reproduce the decoding of the file with the script `discover_cheat_engine.py`. The resulting DEX file is `cheatengine.dex`.

Some important routines of the cheat engine are:

### com.cheats.cheatengine.V.eHS:

Given a byte array, it returns a string with the hexadecimal representation of it.

### com.cheats.cheatengine.V.magic:

Given two byte arrays, it returns the result of the `xor` operation between them. This method is called by several methods of another class of the cheat engine, `StringOp`, which is used to decode some string resources that are stored encoded in the application, for example, some hint-related strings that are printed when the user gets the first cheat right.

### com.cheats.cheatengine.V.test:

This method performs a preliminar verification of the user input, checking the values of some bytes of the string, and returning integer values accordingly. From the application routine that calls this method, we know that the return value should be less than or equal to 33 in order to be a valid cheat. Knowing that, we can find out several characters of the input that compose a valid cheat string.

### com.cheats.cheatengine.V.v:

This method performs the definitive verification of the user input, by comparing the SHA-256 hash of it and a second parameter string, which is always one of the hashes of the cheats, "642385be53489dd39a9256a10a6627dd83e614dacf294de7b0719954a927aeb9" and "7e6fd9ca8c7e437208b5f91efb4a94c568586645345553a25f39c8ef19eae632".


By analysing the code from the `test` method, I found out that the cheat has to be at least 10 characters long, and they have to be, for sure: "R_v_rs_ng__". Since characters 1 and 3 (Considering the string is indexed in [0-9]) have to be equal, I assumed that it was 'e', and from that I concluded that the last character had to be '3', so the string should be something like "Revers_ng_3". I tried strings like "ReversingA3", "Reversinga3", "ReversengA3", etc. but none of them resulted in one of the two SHA-256 hashes of the valid cheats. I tried a script that tested possible characters on the blanks, without any luck. I suppose that the first cheat is something in the form "R_v_rs_ng__", and the second, from the hints I got by reverse-engineering the application, probably is "R_v_rs_ng__EwkaPB0GOyoVU1oWUDcXFzEMAghSVGAwWDZc", because it says to combine the first cheat with "EwkaPB0GOyoVU1oWUDcXFzEMAghSVGAwWDZc" in order to get the second one.