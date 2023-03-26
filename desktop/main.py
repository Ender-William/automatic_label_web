# -*- coding: utf-8 -*-
import os
import sys
import time
from shutil import copyfile
import cv2

import threadUtil
import PySimpleGUI as sg
from configobj import ConfigObj

import service

cur_dir = os.path.dirname(os.path.abspath(__file__))

cfg_path = os.path.join(cur_dir, 'login.ini')
cfg = ConfigObj(cfg_path, encoding='utf8')

if 'LOGIN_INFO' in cfg:
    if 'USERNAME' in cfg['LOGIN_INFO']:
        theme = cfg['LOGIN_INFO']['USERNAME']
        # 应用主题
else:
    cfg['LOGIN_INFO'] = {}


def getAllFilePath(path: str) -> list:
    """
    获取输入路径下的全部的文件的路径
    :param path: str 要检索的路径
    :return: list 返回包含有文件路径的列表
    """
    scan_path = path  # 设置扫描路径
    cur_file_list = os.listdir(scan_path)  # 获取当前目录下的全部路径
    main_file_list = []  # 目录下的所有文件的路径
    for item in cur_file_list:
        # 遍历当前路径下的文件列表中的路径，判断是路径还是文件
        cur_path = os.path.join(scan_path, item)  # 组合路径
        if os.path.isdir(cur_path):
            # 如果是一个路径
            inner_list = getAllFilePath(cur_path)  # 递归获取文件地址
            for inner_item in inner_list:
                main_file_list.append(inner_item)  # 将递归后获取的文件地址加入到主文件路径列表
            inner_list = None  # 释放空间
        else:
            main_file_list.append(cur_path)
    # pmrutils.logUtil.LogSys().show_info(scan_path + " Scan Finish")
    return main_file_list


def login():
    """"""
    sg.theme('GreenMono')
    layout = [
        [sg.Text(text="Auto Label 客户端", size=(15, 1), font='Default 30', text_color='Black', justification='left')],
        [sg.Text(text="用户名", size=(15, 1), font='Default 20', text_color='Black', justification='left')],
        [sg.InputText('', size=(30, 1), font='Default 20', text_color='Black', key='-USERNAME-')],
        [sg.Text(text="密码", size=(15, 1), font='Default 20', text_color='Black', justification='left')],
        [sg.InputText('', size=(30, 1), font='Default 20', text_color='Black', key='-PASSWD-', password_char='*')],
        [sg.Button('登录', font='Default 15', key='-LOGIN-'), sg.Button('取消', font='Default 15')],
        [sg.Text(text="2023 Copyright @ KD_Mercury", size=(25, 1), text_color='Black', justification='left'),
         sg.Text(text="http://blogs.kd-mercury.xyz", size=(23, 1), text_color='Black', justification='left')],
    ]

    window = sg.Window('Auto Label - Login', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        # time.sleep(1)
        event, values = window.read(timeout=10)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        if event == "-LOGIN-":
            username = window['-USERNAME-'].get()
            passwd = window['-PASSWD-'].get()
            if service.login(username, passwd) == "success":
                cfg['LOGIN_INFO']['USERNAME'] = username
                cfg.write()
                break
            else:
                sg.popup("账号或密码错误", font='Default 20')

    # Finish up by removing from the screen
    window.close()


sg.theme('GreenMono')
models = ["1", "2", "3"]
# Define the window's contents
model_choice = [
    [sg.Text(text="模型", size=(4, 1), font='Default 20', text_color='Black', justification='left'),
     sg.Combo(values=models, size=(20, 10), font='Default 20', default_value="1", key="-MODEL-"),
     sg.Button('开始', font='Default 15', disabled=True, key='-START-'),
     sg.Button('停止', font='Default 15', disabled=True, key='-STOP-')],

    [sg.Text(text="选择待处理的文件集", size=(15, 1), font='Default 20', text_color='Black', justification='left'),
     sg.InputText(size=(10, 1), font='Default 20', text_color='Black', key='-PATH-'), sg.FolderBrowse(),
     sg.Button('检索', font='Default 15', key='-SCAN-')]
]
progress_bar = [
    [sg.ProgressBar(max_value=100, orientation='h', size=(51, 62), key='progressbar')]
]
credits = [
    [sg.Text(text="0", size=(5, 1), font='Default 50', text_color='Black', justification='left', key='-CREDITS-')]
]

file_preview = [
    [sg.Listbox(values=models, size=(50, 30), font='Default 15', text_color='Black', key='-PREVIEW-')]
]
processed_file = [
    [sg.Listbox(values=models, size=(50, 30), font='Default 15', text_color='Black', key='-PROCESS-')]
]
# 操作区域的界面展示
operate_area_layout = [
    [sg.Frame(layout=model_choice, title='可用选项', title_color='red', font='Default 10', relief=sg.RELIEF_SUNKEN, ),
     sg.Frame(layout=progress_bar, title='处理进度', title_color='red', font='Default 10', relief=sg.RELIEF_SUNKEN),
     sg.Frame(layout=credits, title='积分', title_color='red', font='Default 10', relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=file_preview, title='文件预览', title_color='red', font='Default 10', relief=sg.RELIEF_SUNKEN),
     sg.Frame(layout=processed_file, title='已处理文件', title_color='red', font='Default 10', relief=sg.RELIEF_SUNKEN)]
]


def start_detect(target_path, path_list):
    processed_finish = []
    window['-PROCESS-'].update(processed_finish)
    # 创建储存文件夹
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        cur_time = str(int(time.time()))
        new_path = target_path + "/" + cur_time
        image_path = new_path + "/" + "images/"
        label_path = new_path + "/" + "labels/"
        if not os.path.exists(new_path):
            os.mkdir(new_path)
            os.mkdir(image_path)
            os.mkdir(label_path)

    if sys.platform.startswith('win32'):
        cur_time = str(int(time.time()))
        new_path = target_path + "\\\\" + cur_time
        image_path = new_path + "\\\\" + "images\\\\"
        label_path = new_path + "\\\\" + "labels\\\\"
        if not os.path.exists(new_path):
            os.mkdir(new_path)
            os.mkdir(image_path)
            os.mkdir(label_path)

    username = cfg['LOGIN_INFO']['USERNAME']
    count_max = len(path_list)
    index = 1
    # print(path_list)
    for pic_path in path_list:
        credits_info = service.get_credits(username)
        model = window['-MODEL-'].get()
        window['-CREDITS-'].update(credits_info)
        print(pic_path)
        try:
            # print(pic_path)
            result = service.get_detect(username, model, pic_path)
            image_name = image_path + str(index) + ".jpg"
            copyfile(pic_path, image_name)
            pic_info = []
            label_name = label_path + str(index) + ".txt"
            label_file = open(label_name, 'a+')
            # print(result)
            for info in result:
                names, cls, x1, y1, x2, y2, conf = info
                content = str(names) + " " + str(cls) + " " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(conf) + "\n"
                label_file.write(content)
                # print(names, cls, x1, y1, x2, y2, conf)
                # pic_info.append(info)
                # print(info)
            label_file.close()
            processed_finish.insert(0, image_name)
            window['-PROCESS-'].update(processed_finish)
        except Exception as e:
            print(e)
        progress = (index / count_max) * 100
        # print(progress)
        window['progressbar'].update(progress)
        index = index + 1


if __name__ == '__main__':
    login()
    # Create the window
    username = cfg['LOGIN_INFO']['USERNAME']
    Window_Name = "Auto Label | User: " + username
    window = sg.Window(Window_Name, operate_area_layout)
    progress_bar = window['progressbar']
    weight = service.get_weights()
    window.read(timeout=10)
    window['-MODEL-'].update(values=weight)
    # Display and interact with the Window using an Event Loop
    while True:
        # 获取积分信息
        credits_info = service.get_credits(username)
        # time.sleep(1)
        event, values = window.read(timeout=1000)
        window['-CREDITS-'].update(credits_info)

        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        if event == '-START-':
            try:
                window['-STOP-'].update(disabled=False)
                window['-START-'].update(disabled=True)
                window['-SCAN-'].update(disabled=True)
                target_path = window['-PATH-'].get()
                file_list = getAllFilePath(target_path)
                detect_thread = threadUtil.MyThread("detect", start_detect, target_path, file_list)
            except:
                pass
        if event == '-STOP-':
            try:
                window['-STOP-'].update(disabled=True)
                window['-START-'].update(disabled=False)
                window['-SCAN-'].update(disabled=False)
                threadUtil.stop_thread(detect_thread)
            except:
                pass
        if event == '-SCAN-':
            window['-START-'].update(disabled=False)
            target_path = window['-PATH-'].get()
            file_list = getAllFilePath(target_path)
            window['-PREVIEW-'].update(file_list)

        # Output a message to the window
    # Finish up by removing from the screen
    window.close()
