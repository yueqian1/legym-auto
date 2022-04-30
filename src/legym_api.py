# -*- coding: UTF-8 -*-

import json
import requests

base_url = 'https://cpes.legym.cn'

login_url = base_url + '/authorization/user/manage/login'
get_current_url = base_url + '/education/semester/getCurrent'
get_activity_url = base_url + '/education/app/activity/getActivityList'
get_course_url = base_url + '/education/course/app/forStudent/list'
get_course_info_url = base_url + '/education/course/app/forStudent/attainability/info'
signup_activity_url = base_url + '/education/app/activity/signUp'
signin_activity_url = base_url + '/education/activity/app/attainability/sign'
signin_course_url = base_url + '/education/course/app/forStudent/sign'

headers = {
    'Content-Type': 'application/json'
}


def req(method, url, headers, data=None, error_text='', params=None):
    response = requests.request(method=method, url=url, headers=headers, data=data, params=params)
    if response.status_code != 200:
        print(error_text + response.text)
        raise Exception(error_text)
    else:
        return json.loads(response.text)


def login(username, password):
    payload = json.dumps({
        'userName': username,
        'password': password,
        'entrance': 1
    })
    response = req(method='POST', url=login_url, headers=headers, data=payload, error_text='登陆出错')
    return User(response['data']['accessToken'], response['data']['id'])


class User:
    def __init__(self, access_token, user_id):
        self.activities = []
        self.courses = []
        self.current = {}
        self.headers = headers
        self.access_token = access_token
        self.headers['Authorization'] = 'Bearer ' + access_token
        self.user_id = user_id
        self.get_current()
        self.get_activities()
        self.get_courses()

    def get_current(self):
        response = req(method='GET', url=get_current_url, headers=self.headers, error_text='获取本周课程信息失败')
        self.current = response['data']

    def get_activities(self):
        payload = json.dumps({
            "name": "",
            "campus": "",
            "page": 1,
            "size": 999,
            "state": "",
            "topicId": "",
            "week": ""
        })
        response = req(method='POST', url=get_activity_url, headers=self.headers, data=payload, error_text='获取活动列表失败')
        self.activities = response['data']['items']

    def get_courses(self):
        response = req(method='GET', url=get_course_url, headers=self.headers, error_text='获取课程列表失败')
        self.courses = response['data']

    def get_course_info(self, course_id):
        params = {
            'courseId': course_id
        }
        response = req(method='GET', url=get_course_info_url, headers=self.headers, params=params,
                       error_text='获取课程信息失败')
        print(response)

    def signup_activities(self, keyword):
        for activity in self.activities:
            if keyword in activity['name']:
                payload = json.dumps({
                    'activityId': activity['id']
                })
                response = req(method='POST', url=signup_activity_url, headers=self.headers, data=payload,
                               error_text='活动报名失败')
                print('活动报名：' + activity['name'] + json.dumps(response, ensure_ascii=False))

    def signin_activities(self, keyword):
        for activity in self.activities:
            if keyword in activity['name']:
                try:
                    payload = json.dumps({
                        'userId': self.user_id,
                        'activityId': activity['id'],
                        'pageType': 'activity',
                        'times': 2,
                        'activityType': 0,
                        'attainabilityType': 2
                    })
                    response = req(method='PUT', url=signin_activity_url, headers=self.headers, data=payload,
                                   error_text='活动签到失败')
                    print('活动签到：' + activity['name'] + json.dumps(response, ensure_ascii=False))
                except:
                    continue

    def signin_course(self, course_id):
        try:
            payload = json.dumps({
                'attainabilityType': "0",
                'courseId': course_id,
                'weekNumber': self.current['weekIndex'],
                'startSignNumber': 1,
                'pageType': 'course',
                'userId': self.user_id
            })
            response = req(method='PUT', url=signin_course_url, headers=self.headers, data=payload,
                           error_text='活动签到失败')
            print('课程签到：' + course_id + json.dumps(response, ensure_ascii=False))
            if '成功' in response['message']:
                return True
            else:
                return False
        except:
            return False
