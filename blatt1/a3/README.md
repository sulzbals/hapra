#   Vulnerabilities

##  1) Stored XSS

### Vulnerability

/card2card echoes the first and last names of the counterparts of the transactions into the response without HTML escaping.

### Possible exploit

One can inject Javascript code wrapped in a script tag in the First and/or Last name fields on /settings, then issue a transaction to another user. When the victim opens /card2card, the echoed script tag is interpreted as a page element and the code is executed.

### Patch

Wrapping the strings echoed in view/standard/card2card.php:47 and :50 with htmlspecialshars() will prevent the script tag from being interpreted as a new element. Therefore, no script will be executed.

##  2) Stored XSS

### Vulnerability

/card2card echoes the message fields of the transactions into the response without HTML escaping.

### Possible exploit

One can inject HTML code to close the input tag, followed by Javascript code wrapped in a script tag in the message field on /card2card/submit, then issue a transaction to another user. When the victim opens /card2card, the echoed script tag is interpreted as a page element and the code is executed.

### Patch

Wrapping the string echoed in view/standard/card2card.php:59 with htmlspecialshars() will prevent the manipulation of tags to insert new elements. Therefore, no script will be executed.
##  3) Stored XSS

### Vulnerability

/card2card/getransactionlogs echoes the logs into the response without HTML escaping.

### Possible exploit

One can inject Javascript code wrapped in a script tag in the message field on /card2card/submit, then issue a transaction to another user. When the user "support" opens /card2card/getransactionlogs, the echoed script tag is interpreted as a page element and the code is executed. This attack is the least likely to succeed from the XSS exploits listed here, because support would have to access /card2card/getransactionlogs via browser, which is unlikely.

### Patch

Wrapping the string echoed in controller/card2card.php:320 with htmlspecialshars() will prevent the script tag from being interpreted as a new element. Therefore, no script will be executed. Support might have to decode the log after retrieving it, but it is safer this way.

##  4) Command execution

### Vulnerability

/index/userlist runs a function that echoes a list of the registered bank's users to any authenticated user.

### Possible exploit

One can retrieve all registered usernames and their respective ids by creating an account and accessing /index/userlist.

### Patch

Changing the statement "else" in controller/index.php:161 to an "elseif" with a condition identical to the one in controller/card2card.php:319 will restrict common users from running the routine that retrieves the user list.

##  5) Command execution

### Vulnerability

/card2card/transactionhistory/$user_id runs a function that echoes a list of all transactions of user with id $user_id to any authenticated user.

### Possible exploit

One can retrieve all user's transactions by accessing /card2card/transactionhistory/$user_id. Notice that $user_id can be retrieved by exploiting vulnerability 4.

### Patch

Adding a condition to the "elseif" statement in controller/card2card.php:303 identical to the one in controller/card2card.php:319 will restrict common users from running the routine that retrieves the transaction history.

##  6) Improper authentication

### Vulnerability

/card2card/export has a form to request the user's transaction history, but the user whose history is retrieved is defined by a POST request parameter.

### Possible exploit

One can retrieve another user's history by accessing /card2card/export, setting the "id" POST parameter to the victim's user id and submitting the request.

### Patch

Wrapping the assignments on controller/card2card.php:212 and :253 inside an if-else statement to retrieve the transactions based on the POST request parameter, if it comes from a support session, or based on the user id associated to the session, if it comes from a normal user session, will keep the export function unrestricted for support and restrict it to common users so they will always get their own data as response.

##  7) Directory traversal

### Vulnerability

/support/iframe only checks the host of the URL before submitting it to libcurl, not the protocol nor the path.

### Possible exploit

One can lead the server to echo the contents of a local file to the response via a cURL FILE request. For example, to get the contents of a local file via cURL, one can pass `file:///absolute/path/to/file` to it. Sending this to /support/iframe will not work because the URL is parsed and cURL is only called if the host of the URL is the same as the host of the server. Although, if one changes it to `file://server_host/absolute/path/to/file`, the host will be the same as the server's, then cURL will be called and output the same as it would by passing the previous URL. The attacker can read any file whose absolute path is known and that can be read by the user www-data in the server.

### Patch

Adding the condition that the parsed scheme must be "http" on controller/support.php:61 will prevent cURL from accessing anything that is not under `http://server_host`. Therefore an attacker will not be able to bypass the server by using a FILE protocol. Updating the error message on :79 is a good practice.

##  8) Plain-text password storage (Bonus)

### Vulnerability

When a given session "PHPSESSID" is created, sensitive user information like username, id, card numbers, session token and, most importantly, password, is written on /tmp/sess_PHPSESSID as plain text.

### Possible (?) exploit

If one knows the "PHPSESSID" of another user's recent session, exploit 7 could be used to steal all that sensitive information. The problem is, how could one steal the "PHPSESSID" of another user? The server sends it to the client as a HttpOnly cookie, making it inacessible through a Javascript client-sided script, then it cannot be stolen by a XSS attack that retrieves "document.cookie", for example.

Although, if one found out how to steal the "PHPSESSID", this one would be the ultimate exploit!

#   Flags

All flags are inserted in the bank by creating a random user, registering a card, and sending the flag to the support user by writing it to the message field of a transaction. Therefore, one can retrieve all flags by getting the transaction history of user support. Both exploits 5 and 6 alone can be used for this, by setting the "id" parameter to "1" (support user's id) and running it.