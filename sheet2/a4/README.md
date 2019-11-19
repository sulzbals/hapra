# Denial of Service

The attack consists of:

1. Spawning a thread to each connection to be tried;

2. Trying all connections in parallel;

## Usage

`python3 dos.py --host [HOST_IP] --port [PORT] --max [MAX_CONNECTIONS]`

## Output

The program should keep printing the status of the connections, then finally printing the maximum supported connections and exiting. This maximum is assumed to be reached when all threads trying to connect either succeeded or failed to connect to the server.