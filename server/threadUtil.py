# -*- coding: utf-8 -*-
import ctypes
import inspect
import threading


class MyThread(threading.Thread):
    """通过继承threading.Thread类创建新的进程"""
    def __init__(self, thread_name, func, *args):
        threading.Thread.__init__(self, name=thread_name)
        '''
        func 传入的应当是函数体
        '''
        self.func = func
        self.args = args

        self.setDaemon(True)
        '''
        主线程运行结束时不对这个子线程进行检查而直接退出，
        同时所有 daemon 值为 True 的子线程将随主线程一起结束，
        而不论是否运行完成。setDaemon 必须在 start 之前调用
        '''
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


def stop_thread(thread):
    """终止进程"""
    _async_raise(thread.ident, SystemExit)


def _async_raise(tid, exctype):
    """这是一个内部方法"""
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")