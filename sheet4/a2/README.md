#   Malware Analysis (Aufgabe 1)

##  Wie tarnt sich die App anfänglich und welchem Zweck dient dies?

The app disguises itself as a simple hacker-themed word cloud, but it actually contains a ransomware which will only run on a real device, since several verifications are made to detect if the application is running in an emulator. If this is the case, the application does nothing.

In order to emulate the ramsonware, I deleted all `System.exit` and `finish` calls from the smali files of the application and repackaged it, then I could observe the malicous activity.

##  Wie ist die Schadroutine der App aufgebaut?

The ransomware:

1. Encodes and steals the contacts of the phone;
2. Adds an event with an alarm on the calendar to constantly warn the user about the ransom (I suppose this is what it does from looking at the source code, but it did not happen when emulating my repackaged version of the application - I might have changed something that altered this behavior, or it might be because Google Calendar wants you to log yourself into your Google account in order to access it, and I obviously was not going to do that);
3. Steals the SMS messages from the phone's inbox;
4. Creates a backdoor that the attacker can use to download the stolen data or run shell commands on the victim's device.

The source code is very tricky because the names of most classes, methods and attributes are just a letter of the alphabet. Apart from that, it is not hard to understand that that the method `j` from `WordCloudActivity` stores the contacts in a array of strings, then deletes the original contact entries, then stores them encoded in a file, or that method `k` from the same class sets a calendar event up, or that `l` stores the SMS messages in a string. What comes after that, on the other hand, is trickier: The class `a` is instantiated, creating a new thread that opens the backdoor.

The backdoor works in the following way:

1. A socket is created and connects to the attacker (`10.20.5.98`);
2. The input stream of the socket is encapsulated in a `PrintWriter` object and the output stream in a `BufferedReader` object;
3. The thread listens to the socket by using the method `BufferedReader.readLine`;
4. When a message is received, it is evaluated whether it is one of the three special functions of the backdor, or a command to be executed. The first case is true if it consists of the name of one of these three functions encoded in base 64: `getSMS` (`Z2V0U01T`), `sendSMS` (`c2VuZFNNUw==`) or `getNr` (`Z2V0TnI=`). Those functions can be used to, respectively, download the SMS inbox of the victim, send a SMS from the victim's device to presumably the attacker's phone number (which is camouflaged by defining an array containing the algarisms 0-9 unordered, then building the phone number by acessing this array) or download the contacts of the victim. If the message is another string, it is interpreted as a shell command instead. The executable name of the shell that is run is camouflaged in the following way: The process is instantiated as `Process exec = Runtime.getRuntime().exec(new String[]{a("iaW4vc2g=", "3RlbS9", "L3N5c"), "-c", str});`, where `str` is the shell command to be run. If you go to the definition of method `a`, you will see that it consists of concatenating the three string parameters in the inverse order, then decoding it in base 64. If you do this step manually, it will result in `/system/bin/sh`, therefore the command `/system/bin/sh -c str` is run on the device;
5. Finally, the data/output of the command requested by the attacker is sent to him by using the method `PrintWriter.println`.

##  Kann die App die Änderungen am System rückgängig machen? Wenn ja, wie?

I did not find any routine to undo the malicious changes, I suppose the attacker would use the backdoor for that.

Although, one could get rid of the ransomware easily without paying the ransom since the contacts are held encoded in a file, they are not completely deleted from the device nor encrypted, so you do not need the attacker in order to restore the data.

##  Schreiben Sie schließlich eine App, welche die von der Schadsoftware verursachten Änderungen rückgängig macht.

The app `YoureWelcome.apk` is able to locate the encoded contacts, decode them and insert them back into the standard contact entries.

It consists of looking up the contacts file stored in the external storage, then decoding them in base 64 (since they were encoded in base 64), then using the Android API to add the contacts back.

In order to work, you have to press the button in the middle of the screen. It will ask for read/write permissions for the contacts and for the external storage. Once the app is allowed, you can restore the contacts by pressing the "Play" button in the lower right corner.