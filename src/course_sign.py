import time

import legym_api
import datetime
import os

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
keyword = os.environ.get('COURSEKEYWORD')

i = 0


def listen_course(course_id):
    interval = 20
    while True:
        global i
        if i >= 270 or user.signin_course(course_id):
            break
        i += 1
        try:
            curr_time = datetime.datetime.now()
            print(datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S') + ':' + course_id)
            time.sleep(interval)
        except:
            time.sleep(interval)
            continue


user = legym_api.login(username, password)
for course in user.courses:
    if keyword in course['name']:
        listen_course(course['id'])
