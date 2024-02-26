from authlib.integrations.requests_client import OAuth2Session
import requests

# Replace these with your actual key and token
api_key = 'd81c7ee6-b208-49d4-a4b4-477cbc8b923e'
access_token = 'e9060152-68cc-449a-a813-72328ea7f8b7'

# Endpoint URL
url = 'https://servicesessentials.ibm.com/apis/v1/curator-ai/executeModel'

# Set the headers with the access token
headers = {
    'x-access-token': f'Bearer e9060152-68cc-449a-a813-72328ea7f8b7'
}

# Make a GET request to the endpoint with the API key as a query parameter and access token in headers
params = {
    'x-security-key': 'd81c7ee6-b208-49d4-a4b4-477cbc8b923e'
}

oauth = OAuth2Session(client_id=None, client_secret=None)
response = oauth.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)


