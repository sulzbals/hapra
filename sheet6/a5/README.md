#   Filereader (Aufgabe 5)

##  Laden Sie sich das Binary filereader und die beiliegende libc.so.6 aus dem StudOn herunter. Ziel ist es, auf der VM 10.0.23.80:31337 eigenen Code auszuführen und die Flagge gespeichert in /home/filereader/flag auszulesen. Dokumentieren Sie außerdem in kurzen Stichpunkten Ihr Vorgehen.

##  1. Schreiben Sie einen Exploit für das Binary filereader, der mit Hilfe der beiliegenden Libc „/bin/sh“ ausführt.
### Tipp: Die Python-Bibliothek https://github.com/Gallopsled/pwntools bietet viele nützliche Features für Binary-Exploitation.
### Tipp: Der Exploit ist deutlich schwieriger mit einer aktuellen Version der Glibc durchzuführen, verwenden Sie deshalb auch zum lokalen Testen des Exploits die beiliegende libc-2.23.

##  2. Führen Sie ihren Exploit remote gegen Host:10.0.23.80, Port:31337 durch und stehlen Sie die Flagge in /home/filereader/flag.
### Hinweis:
### 1. Geben Sie sowohl ihren Exploit als auch die Flagge ab. Der Exploit muss remote gegen die VM funktionieren.
### 2. Die VM hat einen Timeout von 60 Sekunden und schließt danach die Verbindung. Zudem wird alle 10 Minuten ein Hardreset durchgeführt.

fclose+232 == 5dac8