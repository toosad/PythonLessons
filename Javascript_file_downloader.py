import requests

# URL of the JavaScript file
js_file_url = 'my-website.com'

# Sending a GET request to the URL
response = requests.get(js_file_url)

# Check if the request was successful
if response.status_code == 200:
    # Print the content of the file
    print(response.text)
else:
    print("Failed to retrieve the file")
