#!/usr/bin/env python
# coding=utf-8

"""
    作者：刮骨剑
    日期：2021-03-19
    描述：PySimpleGUI 颜色主题
    注：窗口加载完毕后，通过 sg.theme('theme_name') 方法直接应用主题是无法立即生效的，所以在这里构造了两种方式来应用主题：1、通过加载子窗口来生成预览；2、选择主题后保存到配置文件中，再重启程序自身，使下次加载窗口前能读取到上次已选择的主题并应用；
"""

import os, sys, time, random
import PySimpleGUI as sg
from configobj import ConfigObj


def restart_program():
    """重启程序"""
    # 获取 Python 解释器的路径
    python_path = sys.executable
    # 获取程序路径
    program_path = os.path.abspath(__file__)
    # 重启程序
    os.execl(python_path, program_path, *sys.argv)


cur_dir = os.path.dirname(os.path.abspath(__file__))

cfg_path = os.path.join(cur_dir, '颜色主题.ini')
cfg = ConfigObj(cfg_path, encoding='utf8')

# 获取主题列表
themes = sg.theme_list()

# 从配置文件中获取主题
if 'ColorTheme' in cfg:
    if 'theme' in cfg['ColorTheme']:
        theme = cfg['ColorTheme']['theme']
        # 应用主题
        sg.theme(theme)
else:
    cfg['ColorTheme'] = {}

# 定义布局
layout = [
    [sg.Text('请选择一个主题：')],
    [sg.Listbox(values=themes, size=(40, 12), key='listbox_theme_list', enable_events=True)],
    [sg.Text('已选择的主题：', size=(12, 1)), sg.Text('', size=(28, 1), key='text_theme_selected')],
    [sg.Text('当前主题：', size=(12, 1)), sg.Text(sg.theme(), size=(28, 1), key='text_theme_cur')],
    [
        sg.Button('应用已选择的主题', key='bt_apply_theme_selected'),
        sg.Button('随机更换主题', key='bt_change_theme_random'),
        sg.Button('退出', key='bt_exit')
    ]
]

# 创建窗口
window = sg.Window('主题浏览器', layout, font=('YaHei Consolas Hybrid', 15))


def theme_prev(theme):
    '''主题预览'''
    layout = [
        [sg.T(theme, size=(20, 2))],
        [sg.Button('退出', size=(20, 2), key='bt_exit')]
    ]
    win_prev = sg.Window('主题预览', layout, font=('YaHei Consolas Hybrid', 15), keep_on_top=True)
    event_prev, values_prev = win_prev.read()
    # print(event_prev, values_prev)
    while True:
        if event_prev in (sg.WIN_CLOSED, 'bt_exit'):
            break
    win_prev.close()


# 事件循环
while True:
    event, values = window.read()
    # print(event, values)
    if event == 'listbox_theme_list':
        theme_list = values['listbox_theme_list']
        theme = theme_list[0]
        # 更新已选择的主题
        window.Element('text_theme_selected').Update(value=theme)
        # 主题预览
        sg.theme(theme)
        theme_prev(theme)
    if event == 'bt_apply_theme_selected':
        theme_list = values['listbox_theme_list']
        if theme_list == []:
            sg.popup_error('未选择有效的主题！', no_titlebar=True)
        else:
            theme = theme_list[0]
            # 主题保存到配置文件
            cfg['ColorTheme']['theme'] = theme
            cfg.write()
            # 重启程序，以应用主题
            restart_program()
    if event == 'bt_change_theme_random':
        # 随机获取一个主题
        theme = random.choice(themes)
        # 主题保存到配置文件
        cfg['ColorTheme']['theme'] = theme
        cfg.write()
        # 重启程序，以应用主题
        restart_program()
    if event in (sg.WIN_CLOSED, 'bt_exit'):
        break

# 关闭窗口
window.close()

