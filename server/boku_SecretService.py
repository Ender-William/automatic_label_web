# -*- coding: utf-8 -*-
import pymysql


class DBUtils:

    def __init__(self):
        """数据库初始化"""
        host = "127.0.0.1"
        port = 3306
        user = 'root'
        passwd = "02.05.09kd"
        charset = 'utf8'
        database = 'AutoLabel'
        self.conn = pymysql.connect(host=host, port=port,
                                    user=user, passwd=passwd,
                                    charset=charset, db=database)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def is_user_exist(self, username: str) -> bool:
        """
        查询用户是否存在
        :param username: 用户名
        :return: 存在 True 不存在 False
        """
        sql = "select username from account where username= %s"
        self.cursor.execute(sql, [username])
        self.conn.commit()
        data_list = self.cursor.fetchall()
        if len(data_list) == 0:
            # 没有查询到
            return False
        else:
            return True

    def add_user(self, username: str, passwd: str, phone: str) -> bool:
        """
        添加用户
        :param username: 用户名
        :param passwd: 密码
        :param phone: 手机号
        :return: 注册成功 True 注册失败 False
        """
        # 判断用户是否存在
        if not self.is_user_exist(username=username):
            # 如果存在
            # login_state 为 0 时表明未登录
            # account_state 为 0 时表明账号注销，为 1 时表明账号未注销
            sql = "insert into account(username,passwd,phone,login_state,account_state) values(%s,%s,%s,0,1)"
            # 提交 SQL 语句
            self.cursor.execute(sql, [username, passwd, phone])
            self.conn.commit()
            if self.is_user_exist(username=username):
                # 如果用户存在
                sql = "insert into credits(username,credits,onlineTime) values(%s,'10000','0000-00-00')"
                # 提交 SQL 语句
                self.cursor.execute(sql, [username])
                self.conn.commit()
                return True
            else:
                return False
        else:
            return False

    def login(self, username: str, passwd: str) -> bool:
        """
        登录查询
        :param username: 用户名
        :param passwd: 密码
        :return: 账号密码正确 True 任一参数错误 False
        """
        sql = "select username,passwd from account where username= %s and passwd = %s"
        self.cursor.execute(sql, [username, passwd])
        self.conn.commit()
        data_list = self.cursor.fetchall()
        print(len(data_list))
        if len(data_list) == 0:
            # 账号或密码错误
            return False
        else:
            sql = "update account set login_state = '1' where username = %s"
            self.cursor.execute(sql, [username])
            self.conn.commit()
            return True

    def get_credits(self, username: str) -> int:
        """
        查询指定用户的积分
        :param username: 用户名
        :return: 积分数量
        """
        # 查询用户是否处于登录状态
        sql = "select credits from credits where username= %s"
        self.cursor.execute(sql, [username])
        self.conn.commit()
        data_list = self.cursor.fetchall()
        if len(data_list) == 0:
            # 没有查询到
            return False
        else:
            return data_list[0]['credits']

    def update_credits(self, username, credits):
        """
        更新指定用户的积分
        :param username:
        :param credits:
        :return:
        """
        sql = "update credits set credits = %s where username = %s"
        self.cursor.execute(sql, [credits, username])
        self.conn.commit()

    def get_model(self):
        sql = 'select model from model'
        self.cursor.execute(sql)
        self.conn.commit()
        data_list = self.cursor.fetchall()
        return data_list


    def close(self):
        # 关闭 SQL 链接
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    # print(DBUtils().add_user("123","123","123"))
    # print(DBUtils().is_user_exist(username="admin"))
    # print(DBUtils().login(username="admin", passwd="admin1232"))
    print(DBUtils().get_credits("admin"))
    DBUtils().close()
