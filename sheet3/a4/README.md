#   Rootkit

##  Description

The rootkit hides files (or whole directories), processes and connections, as well as itself. This is achieved by:

### Files

By hooking the `getdents` system call, so if a directory entry has a filename that the rootkit is supposed to hide, it is not written to the user-space buffer.

### Processes

In UNIX almost everything is a file, including processes. The rootkit uses `getdents` hooking as well to hide an arbitrary process.

### Connections

By hooking tcp, tcp6, udp and udp6 protocol functions so if there is a connection whose source port the rootkit is supposed to hide, it is not returned to the user.

##  Installation

To install the rootkit, run as root:

`./install.sh [FILE_TO_BE_HIDDEN] [PID_TO_BE_HIDDEN] [PORT_TO_BE_HIDDEN]`