# HTTP Fingerprinting

The algorithm consists of:

1. Using raw sockets to determine which ports are open by scaning all possible ports of the server - This step is VERY slow. Please be patient...;

2. Using the requests library to send HTTP requests to each open port;

3. Parsing the headers of the valid HTTP responses received to extract the name of the HTTP server (daemon) that runs on the respective port.

## Usage

`python3 http_fingerprinting.py --ip [HOST_IP]`

## Output

The program should print a relation between all encountered daemons and the ports they run on.

# FTP Fingerprinting

The algorithm consists of:

1. Sending a message specifying a random login username to each port;

2. Entering the bodies of the responses in a lookup table to determine which FTP daemon runs on the respective port.

This lookup table was built after a little research about the text message each FTP server sends with a 331 (ask for user's password) response. Check the comments in the code for more details.

## Usage

`python3 ftp_fingerprinting.py --ip [HOST_IP]`

## Output

The program should print a relation between the daemons and the ports they run on.