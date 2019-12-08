#   Skiddy’s First Steps (Aufgabe 1)

##  Entpacken Sie die APK und analysieren Sie den Source Code. Welche Credentials sind in der App hinterlegt?

On de/fau/i1/aka/h4ckpro/LoginActivity.class:35:

`private static final String[] DUMMY_CREDENTIALS = new String[] { "YmFiYnlzQGZpcnN0LnJlOnBhY2thZ2VkLmFwcA==" };`

##  Analysieren Sie die Analyseroutinen, welche die App nach der Anmeldung vornimmt. Die App versucht Repackaging, Debugging, dynamische Analyse und Emulatoren zu erkennen. Schreiben Sie zu jeder Analyseroutine wonach gesucht wird und warum.

### de/fau/i1/aka/h4ckpro/anal/DbgAnal.class (debugging):

It checks if the application's UID and flags are different than the expected values, therefore detecting if the applications is being debugged.

### de/fau/i1/aka/h4ckpro/anal/DyAnal.class (dynamic analysis):

It checks if some system properties are different than the expected values, therefore detecting if the applications is being dynamically analysed.

### de/fau/i1/aka/h4ckpro/anal/EmAnal.class (emulators):

It checks if the build fingerprint contains the `sdk` string, therefore detecting if the application is being emulated.

### de/fau/i1/aka/h4ckpro/anal/InAnal.class (repackaging):

It compares the SHA1 fingerprint of the first package signature with a constant value defined in the class. The purpose of this comparison is detecting if the package was signed by a different key, therefore detecting if there was a repackaging.

##  Patchen Sie die APK und packen Sie sie neu, so dass die Routinen nie etwas erkennen.

This can be easily achieved by deleting the lines de/fau/i1/aka/h4ckpro/ProtectionActivity.smali:49 and :58, then rebuilding the package. By doing this, the if-statement that evaluates the return value of the analysis routine is removed. This means that the `update` routine will always be called, therefore the "result" of each analysis will be always `SOLVED`.