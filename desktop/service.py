# -*- coding: utf-8 -*-
import base64
import numpy as np
import requests, time, json
import cv2
from PIL.Image import Image

URL = "http://127.0.0.1:5000"


def login(username, passwd):
    url = URL + "/login"
    res = requests.post(url, data={'username':username, 'passwd': passwd})
    res_json = json.loads(res.text)
    return res_json['login']


def get_credits(username):
    url = URL + "/getcredits"
    res = requests.get(url, data={'username': username})
    res_json = json.loads(res.text)
    return res_json

def get_detect():
    url = URL + "/detect"
    cap = cv2.imread('WIN_20230123_14_33_16_Pro.jpg')
    # with open('0.jpg', 'rb+') as f:
    #     data_base64 = base64.b64encode(f.read())
    #     data_base64 = data_base64.decode()
    str_img = str(base64.b64encode(cv2.imencode('.jpg',cap)[1]))[2:-1]
    res = requests.post(url, data={'img':str_img})
    print(res.text)
    res_json = json.loads(res.text)
    print(res_json)

if __name__ == '__main__':
    # print(login("admin", "admin123"))
    # print(get_credits("admin"))
    get_detect()