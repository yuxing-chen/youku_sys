# Author:Cecilia

from orm import mysql_contorl



# 字段类，所有字段类的父类
class Fields:
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


# 整型字段类
class Integer(Fields):
    def __init__(self,name,column_type='int',primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)


# 字符型数据类
class String(Fields):
    def __init__(self, name, column_type='varchar(250)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)






# 元类，控制表类对象的产生
class MyMetaclass(type):
    def __new__(cls, class_name,class_base,class_attr):
        if class_name == 'Models':
            return  type.__new__(cls, class_name,class_base,class_attr)

        table_name = class_attr.get('table_name',class_name)
        mappings = {}
        primary_key = None

        for k,v in class_attr.items():
            if isinstance(v,Fields):
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise  TypeError('一个表只能有一个主键 ！')
                    else:
                        primary_key = v.name

        if not primary_key:
            raise TypeError('一个表必须有一个主键 ！')

        for k in mappings.keys():
            class_attr.pop(k)

        class_attr['table_name'] = table_name
        class_attr['primary_key'] = primary_key
        class_attr['mappings'] = mappings
        return type.__new__(cls, class_name, class_base, class_attr)



# 所有表类的父类，通过继承字典实现字典可以用点取值赋值
class Models(dict,metaclass=MyMetaclass):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


    #字典点赋值时触发
    def __setattr__(self, key, value):
        self[key] = value

    # 字典点取值时触发
    def __getattr__(self, item):
        return self.get(item)



    # 类的绑定方法，类可以不用传第一个参数可以直接用，对象也可以不用传第一个参数用
    @classmethod
    def select(cls,**kwargs):
        mysql_obj =  mysql_contorl.MySQL()
        if not kwargs:
            sql = 'select * from %s' %cls.table_name
            res = mysql_obj.select(sql)
        else:
            key = list(kwargs.keys())[0]
            value = kwargs.get(key)
            sql = 'select * from %s where %s=?'%(cls.table_name,key)
            sql = sql.replace('?','%s')
            res = mysql_obj.select(sql,value)
        return [cls(**r) for r in res]


    # 向数据库中插入数据
    def save(self):
        mysql_obj =  mysql_contorl.MySQL()

        # insert into table() values()

        keys=[]
        values=[]
        replace = []
        for k,v in self.mappings.items():
            keys.append(k)
            values.append(getattr(self,v.name,v.default))
            replace.append('?')

        sql = 'insert into %s(%s) values(%s)'%(self.table_name,','.join(keys),','.join(replace))
        sql = sql.replace('?','%s')
        mysql_obj.execute(sql,values)


    # 修改数据库中的数据
    def sql_update(self):
        mysql_obj = mysql_contorl.MySQL()

        keys = []
        primary_key = None
        values = []
        for k,v in self.mappings.items():
            if v.primary_key:
                primary_key = getattr(self,v.name,v.default)
            else:
                keys.append(v.name+'=?')
                values.append(getattr(self,v.name,v.default))

        sql = 'update %s set %s where %s=%s' %(self.table_name,','.join(keys),self.primary_key,primary_key)
        sql = sql.replace('?','%s')
        mysql_obj.execute(sql,values)




