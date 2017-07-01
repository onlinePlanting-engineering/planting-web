import requests

baseUrl = 'http://127.0.0.1:8080'

token = '63a5f8bb70efb7d2d38282db840dba702b18d1c2'
headers = {
    'Content-type': 'multipart/form-data',
    'Accept': 'application/json',
    'Authorization': 'Token {}'.format(token)
}

data = 'nickname=icnbrave'

respose = requests.put(
    url='{base_url}/api/profiles/13/'.format(base_url=baseUrl),
    data=data,
    headers=headers
).json()
print(respose)
