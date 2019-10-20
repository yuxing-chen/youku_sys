# Author:Cecilia
import pymysql


# 数据库类
class MySQL:

    # 单例模式，控制同一个对象的重复创建
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance



    # 连接数据库
    def __init__(self):
        self.mysql = pymysql.connect(host='127.0.0.1',
                                     port=3306,
                                     user='root',
                                     password='123',
                                     database='orm_demo',
                                     charset='utf8',
                                     autocommit=True)


        # 创建游标对象
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)


    # 对数据库查询数据
    def select(self,sql,args=None):
        self.cursor.execute(sql,args)
        res  = self.cursor.fetchall()
        return res

    # 向数据库提交数据
    def execute(self,sql,args):
        try:
            self.cursor.execute(sql, args)
        except Exception as e:
            print(e)
            print(sql)

