# -*- coding: utf-8 -*-
import base64

import cv2
from flask import Flask, request
import boku_SecretService as bss
import yolo_detectAPI
import torch
import types
import numpy as np

app = Flask(__name__)

@app.route('/livecheck', methods=['POST'])
def livecheck():
    return {"live": "yes"}


@app.route('/login', methods=['POST'])
def login():
    # 获取用户名和密码
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    DBUtil = bss.DBUtils()

    if DBUtil.login(username=username, passwd=passwd):
        DBUtil.close()
        return {"login": "success"}
    DBUtil.close()
    return {"login": "false"}

@app.route('/getcredits', methods=['GET'])
def getcredits():
    username = request.form.get('username')
    DBUtil = bss.DBUtils()
    credits = DBUtil.get_credits(username=username)
    DBUtil.close()
    return credits

@app.route('/detect', methods=['POST'])
def detect():
    img = request.form.get('img')
    username = request.form.get('username')
    DBUtil = bss.DBUtils()
    credits = int(DBUtil.get_credits(username=username))
    if credits == 0:
        return []
    else:
        credits = credits - 1
        DBUtil.update_credits(username=username, credits=credits)
    DBUtil.close()
    image = base64.b64decode(img)
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    with torch.no_grad():
        result, names = yolo_model.detect([img])
        # 每一帧图像的识别结果（可包含多个物体）
        recog_list = []
        for cls, (x1, y1, x2, y2), conf in result[0][1]:
            recog_list.append([names, cls, x1, y1, x2, y2, conf])  # 识别物体种类、左上角x坐标、左上角y轴坐标、右下角x轴坐标、右下角y轴坐标，置信度
    print(recog_list)
    return recog_list


if __name__ == '__main__':
    yolo_model = yolo_detectAPI.DetectAPI(weights='./weight/five_gesture.pt')
    app.run()