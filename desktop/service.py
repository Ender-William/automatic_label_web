# -*- coding: utf-8 -*-
import base64
import os

import requests, time, json
import cv2
from configobj import ConfigObj

URL = "http://127.0.0.1:5000"


def login(username, passwd):
    url = URL + "/login"
    res = requests.post(url, data={'username': username, 'passwd': passwd})
    # print(res.text)
    res_json = json.loads(res.text)
    return res_json['login']


def get_credits(username):
    url = URL + "/getcredits"
    res = requests.get(url, data={'username': username})
    # print(res.text)
    res_json = json.loads(res.text)
    return res_json


def get_detect(username, model, img_path):
    url = URL + "/detect"
    cap = cv2.imread(img_path)
    # with open('0.jpg', 'rb+') as f:
    #     data_base64 = base64.b64encode(f.read())
    #     data_base64 = data_base64.decode()
    str_img = str(base64.b64encode(cv2.imencode('.jpg', cap)[1]))[2:-1]
    res = requests.post(url, data={'username': username, 'img': str_img, 'model': model})
    print(res.text)
    res_json = json.loads(res.text)
    return res_json
    # print(res_json)


def get_weights():
    url = URL + "/getweight"
    res = requests.get(url)
    res_json = json.loads(res.text)
    model = []
    for item in res_json:
        model.append(item['model'])
    return model


if __name__ == '__main__':
    # print(login("admin", "admin123"))
    # print(get_credits("admin"))
    print(get_weights())
