import requests

s = requests.Session()

r = s.get("http://10.0.23.24:8005/level05/")

# The last two lines of the response are the secret and the operation to be solved.
lines = r.text.splitlines()[-2:]

secret = lines[0].split()[-1]			# The secret is only the last word.
result = eval(lines[1].split(": ")[1])	# The result is the evaluation of what comes after the ": ".

# Submit the solution to the challenge.
r = s.post("http://10.0.23.24:8005/level05/", data={"secret":secret, "result":result})

# Print HTML response
print(r.text)