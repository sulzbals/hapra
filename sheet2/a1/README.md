## HTTP Fingerprinting

The algorithm consists on:

1. Using raw sockets to determine which ports are open by scaning all possible ports of the server;

2. Using the requests library to send a HTTP request to each open port;

3. Parsing the headers of the valid HTTP responses received to extract the name of the HTTP server (daemon) that runs on the respective port.

## FTP Fingerprinting

The algorithm consists on:

1. Sending a message specifying a random login username to each port;

2. Entering the bodies of the responses in a lookup table to determine which FTP daemon runs on the respective port.