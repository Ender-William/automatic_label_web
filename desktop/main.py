# -*- coding: utf-8 -*-
import os

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


def login():
    """"""
    sg.theme('GreenMono')
    layout = [
        [sg.Text(text="Auto Label 客户端", size=(15, 1), font='Default 30', text_color='Black', justification='left')],
        [sg.Text(text="用户名", size=(15,1), font='Default 20', text_color='Black', justification='left')],
        [sg.InputText('', size=(30,1), font='Default 20', text_color='Black', key='-USERNAME-')],
        [sg.Text(text="密码", size=(15, 1), font='Default 20', text_color='Black', justification='left')],
        [sg.InputText('', size=(30,1), font='Default 20', text_color='Black', key='-PASSWD-', password_char='*')],
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
models = ["1","2","3"]
# Define the window's contents
model_choice = [
    [sg.Text(text="请选择要使用的模型", size=(15,1), font='Default 20', text_color='Black', justification='left'),
     sg.Combo(models, size=(10,10), font='Default 20', default_value="1", key="-MODEL-"),
     sg.Button('开始', font='Default 15', key='-START-'), sg.Button('停止', font='Default 15', key='-STOP-')],

    [sg.Text(text="选择待处理的文件集", size=(15,1), font='Default 20', text_color='Black', justification='left'),
     sg.InputText(size=(15,1), font='Default 20', text_color='Black'),sg.FolderBrowse(key='PATH')]
]
progress_bar = [
    [sg.ProgressBar(max_value=100, orientation='h', size=(51, 62), key='progressbar')]
]
credits = [
    [sg.Text(text="0", size=(5,1), font='Default 50', text_color='Black', justification='left', key='-CREDITS-')]
]

file_preview = [
    [sg.Listbox(values=models, size=(50,30), font='Default 15', text_color='Black', key='-PREVIEW-')]
]
processed_file = [
    [sg.Listbox(values=models, size=(50,30), font='Default 15', text_color='Black', key='-PROCESS-')]
]
# 操作区域的界面展示
operate_area_layout = [
    [sg.Frame(layout=model_choice, title='可用选项',title_color='red', font='Default 10',relief=sg.RELIEF_SUNKEN,),
     sg.Frame(layout=progress_bar, title='处理进度',title_color='red', font='Default 10',relief=sg.RELIEF_SUNKEN),
     sg.Frame(layout=credits, title='积分',title_color='red', font='Default 10',relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=file_preview, title='文件预览',title_color='red', font='Default 10',relief=sg.RELIEF_SUNKEN),
     sg.Frame(layout=processed_file, title='已处理文件',title_color='red', font='Default 10',relief=sg.RELIEF_SUNKEN)]
]


if __name__ == '__main__':
    login()
    # Create the window
    window = sg.Window('Auto Label', operate_area_layout)
    progress_bar = window['progressbar']
    username = cfg['LOGIN_INFO']['USERNAME']
    # 获取积分信息
    credits_info = service.get_credits(username)
    # Display and interact with the Window using an Event Loop
    while True:
        # time.sleep(1)
        event, values = window.read(timeout=10)
        window['-CREDITS-'].update(credits_info)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        # Output a message to the window
    # Finish up by removing from the screen
    window.close()
