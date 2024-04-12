import requests

url = 'https://google.com'
response = requests.get(url)

print("Response Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Content:", response.text)