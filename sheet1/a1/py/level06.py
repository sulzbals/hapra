import requests
from html.parser import HTMLParser

class MyParser(HTMLParser):
    # Initiate a list inside the instance to store parsed data.
	def init_list(self):
		self.list = list()

    # Only those words have 32 characters in the HTML response, so we can use this criteria
    # to parse and store them in the list.
	def handle_data(self, data):
		line = "{}".format(data).split()
		if line:
			if len(line[0]) == 32:
				self.list.append(line[0])

# Instantiate one parser for each request.
parser1 = MyParser()
parser2 = MyParser()

# Initiate lists.
parser1.init_list()
parser2.init_list()

# We want two requests from the same session.
s = requests.Session()

# Make two requests.
r1 = s.get("http://10.0.23.24:8005/level06/")
r2 = s.get("http://10.0.23.24:8005/level06/")

# Each parser parses one of the responses.
parser1.feed(r1.text)
parser2.feed(r2.text)

# Get the one word from the second response that does not exist in the first response.
for line in parser2.list:
	if line not in parser1.list:
		new_value = line
		break

# Submit the different word to the challenge.
r = s.post("http://10.0.23.24:8005/level06/", data={"new_value":new_value})

# Print HTML response
print(r.text)