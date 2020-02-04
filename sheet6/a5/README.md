#   Filereader (Aufgabe 5)

##  1. Schreiben Sie einen Exploit für das Binary filereader, der mit Hilfe der beiliegenden Libc „/bin/sh“ ausführt.

The exploit consists mainly of a buffer overflow on the `name` buffer stored on the `.bss` section. This buffer is used when the user sends an "Exit" command to `filereader`: It asks for the user's name, and stores whatever input given by the user on the buffer, without any kind of bound checking. The variable `fp` is located right after this buffer, and therefore is overwritten when it overflows.

`fp` points to the `FILE` structure that is allocated when the program opens a file. If the "Exit" command is given to `filereader` while there is an open file, `fp` is passed as parameter to `fclose`, which closes the file before exitting the program. A `FILE` struct has a field called `vtable`, which points to a table containing the addresses of functions that can be used to perform operations with the file associated to this structure (`open`, `read`, `write`, etc.). `fclose` uses this virtual table to call the `close` routine.

Knowing all this, the following input can be fed to the program in order to overflow the `name` buffer and hijack the instruction pointer and redirect the execution flow to an arbitrary address:

1. 32 padding bytes to fill the whole `name` buffer;
2. An address that points to the word located right after it (this makes `fp` point to `&fp+0x4`);
3. A crafted `FILE` struct, whose field `vtable` points to the address right after it (`&vtable+0x4`)
4. A crafted virtual table that will be pointed by `vtable`, populated with several copies of the address we want to jump to.

After doing this, `fp` will point to the injected `FILE` structure, and its `vtable` will point to the table injected right after it. When `fclose` is called, it will access something like `fp->vtable->close` and call it as a function, redirecting the execution flow to the address we injected.

So now we can change the execution flow to wherever we want. But which location will cause the program to run `/bin/sh`? There is nothing useful on the program itself, so the only way is redirecting it to an address of `libc`. The problem is that `libc` is a shared library, mapped to a random address by the dynamic linker when the program is executed.

One way to get the base address of `libc` on the virtual addressing space of a running `filereader` process is looking at `/proc/PID/maps`, where `PID` is the id of the process. Locally, this is easy to find out, but we just do not know about the one running on the remote server. I will cover the remote server approach on the next exercise's solution, and for now just proceed with the local process part and assume we just know the `PID` of a running `filereader`.

The `filereader` itself can be used to read `/proc/PID/maps`. Once we know the address `libc` is mapped to, we can add it to the offset (address) of the instruction we want to redirect the flow to. We can redirect it to `system()` in order to run `/bin/sh`.

`system()` expects a pointer to the command line to be executed on register `ESI`, and `fclose` has set it to `fp`, so it will try to interpret our injected `FILE` struct as a string. We could write `/bin/sh` to the beginning of the structure, but that would overwrite the `flags` field and potentially change `fclose` behavior. I solved this problem by writing `;/bin/sh` on the fields after `flags`, so `system()` will try to run the binary data of the `flags` field as a command (which will not work), then will run `/bin/sh` as a separate command because of the `;`.

This is how you can exploit `filereader` to run `/bin/sh`. I wrote a python script that performs this attack using `pwntools`. You can use `python3 exploit.py --local` to check it out.

##  2. Führen Sie ihren Exploit remote gegen Host:10.0.23.80, Port:31337 durch und stehlen Sie die Flagge in /home/filereader/flag.

As mentioned before, the exploit described on the previous solution can only be used if the `PID` of `filereader` is known, which is not the case when running it on the remote host. I solved this by adding a step on the exploit to find out the `PID` by brute-force.

The brute-forcing consists of trying to access and read `/proc/PID/cmdline` for all valid `PID`s until a command line containing `filereader` is found. Once we know this is the process id from the `filereader` instance running on the remote server, we can just go through it with the previously described exploit to spawn `/bin/sh`.

The same script can be used to perform the attack against the remote host. Just run `python3 exploit.py --remote`. The host and port can be passed as arguments if needed, run with `--help` to check out.

Once I had a shell running on the remote host, the first thing I tried in order to steal the flag was running `cat /home/filereader/flag`. This did not work, because I was user `filereader`, and the flag file is owned by the user `flag`, and only it has read permission to the file.

So I inspected the contents of `/home/filereader`, and noticed the files `get_flag` and `get_flag.c` conveniently placed there. Despite both files being owned by `flag` as well, `filereader` has read permission to the source code and executing permission to the executable, so it was just a matter of seeing how it works and then running it to retrieve the flag.

The program asks for a "magic" password, which is `Give me the flag`. By giving this as input, the flag was printed:

`$ cd /home/filereader`<br>
`$ ./get_flag`<br>
`Your magic :$ Give me the flag`<br>
`Here is your flag: FLAG{F1l3_Str34m_is_4w3s0m3}`<br>
`\x7f `<br>
`$`<br>
