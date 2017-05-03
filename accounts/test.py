from django.test import TestCase
import requests,json

def printJson(json_obj):
    print(json.dumps(json_obj, indent=4, sort_keys=True))

user_info = {
    'username':'18082371886',
    'password':'q1w2e3r4',
}

base = 'http://localhost:8080'
list_users = '{0}/api/users/'.format(base)
login_url = '{0}/api/users/login/'.format(base)
register_url = '{0}/api/users/register/'.format(base)

get_auth_token_url = '{0}/api/users/get_auth_token/'.format(base)
get_current_user_info_url = '{0}/api/users/user_info/'.format(base)
user_info_url_pattern = '{0}/api/users/%s/'.format(base)

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

res = requests.post(login_url, json=user_login)
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

print('------ Get current user infomatioin ----')
current_user_info = response3 = requests.get(get_current_user_info_url, headers=headers2).json()
printJson(current_user_info)


print('--------- Get current user profile ------')
uid = current_user_info['data']['id']
user_profile_url = user_info_url_pattern % (uid)
user_profile = requests.get(user_profile_url, headers=headers2).json()
printJson(user_profile)

# print('-------- Update user profile --------')
# headers2.update({'Content-Type': 'multipart/form-data'})
# user_profile['profile']['img_heading'] = open('/Users/frankin/dev/fuzhiyong1.png', 'rb')
# files = {'img_heading' : open('/Users/frankin/dev/fuzhiyong1.png', 'rb')}
# response4 = requests.put(user_profile_url, data=user_profile, files=files, headers=headers2)
# print(response4)