from django.test import TestCase
import requests,json

def printJson(json_obj):
    print(json.dumps(json_obj, indent=4, sort_keys=True))

user_info = {
    'username':'frankin5',
    'password':'q1w2e3r4',
    'email':'zhiyongf@126.com',
    'email2':'zhiyongf@126.com'
}

base = 'http://localhost:8080'
list_users = '{0}/api/users/'.format(base)
login_url = '{0}/api/users/login/'.format(base)
register_url = '{0}/api/users/register/'.format(base)

get_auth_token_url = '{0}/api/users/get_auth_token/'.format(base)

print('--------- Try to get users without authentication ------------')
response = requests.get(list_users)
print(response.status_code)
printJson(response.json())


print('------------- Try to reister a user  -------------')
headers = {
    'Content-Type': 'application/json'
}
response = requests.post(register_url, json=user_info)

print('-------- try to get token of the specific user ----------')
user_login = {
    'username': user_info.get('username'),
    'password': user_info.get('password')
}

res = requests.post(get_auth_token_url, json=user_login)
print(res.status_code)
printJson(res.json())
token = res.json().get('token', None)
print('Token: {0}'.format(token))

print('------- Get user list again with token in request header ---------')
headers2 = {
    'Authorization': 'Token {0}'.format(token)
}
response2 = requests.get(list_users, headers=headers2)
print(response2.status_code)
printJson(response2.json())