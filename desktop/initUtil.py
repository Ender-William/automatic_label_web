# -*- coding: utf-8 -*-
import configparser
import logUtil as logUtil


def config_reader(ini_path, section, key):
    """
    读取 ./config.ini 文件
    :param ini_path: 文件地址
    :param section: section
    :param key: options
    :return: value
    """
    config = configparser.ConfigParser()
    config.read(ini_path, encoding="utf-8")
    value = config.get(section, key)
    return value


def config_writter(ini_path, section, key, value):
    """
    写入 init 文件
    :param ini_path: 文件地址
    :param section: section
    :param item_name: option
    :param value: value
    :return:
    """
    try:
        config = configparser.ConfigParser()
        config.read(ini_path, encoding="utf-8")
        config.set(section, key, value)

        # 保存配置
        config.write(open(ini_path, "w"))

        # 记录
        logUtil.LogSys() \
            .show_warning("Utils.stringUtil.config_writter config change save!")

    except:
        logUtil.LogSys() \
            .show_warning("Utils.stringUtil.config_writter config file not exist!")
