import os
import legym_api

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
keyword = os.environ.get('KEYWORD')

user = legym_api.login(username, password)
user.signup_activities(keyword)
user.signin_activities(keyword)
