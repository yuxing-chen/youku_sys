# Author:Cecilia
import struct
import json
import hashlib
import uuid
from functools import wraps
from db import user_data,models



# 服务端向客户端发送数据
def send_msg(send_dic,conn,file_path=None):
    json_data = json.dumps(send_dic).encode('utf8')
    headers = struct.pack('i',len(json_data))
    conn.send(headers)
    conn.send(json_data)

    if file_path:
        with open(file_path,'rb') as fr:
            for line in fr:
                conn.send(line)







# 获取密码的MD5值，用户存在数据库里
def get_pwd_md5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf8'))
    sql = 'user'
    md5.update(sql.encode('utf8'))
    return md5.hexdigest()





# 获取用户登录成功的随即加密字符串做为标识
def get_session_md5(name):
    md5 = hashlib.md5()
    md5.update(name.encode('utf8'))
    uuid_obj  =uuid.uuid4()
    md5.update(str(uuid_obj).encode('utf8'))
    return md5.hexdigest()







def login_auth(func):
    @wraps(func)
    def inner(*args,**kwargs):
        back_dic = args[0]
        session = back_dic.get('session')
        addr = back_dic.get('addr')


        user_data.metux.acquire()
        session_id = user_data.online_user.get(addr)
        user_data.metux.release()
        if session_id:
            if session_id[0] == session:
                args[0]['user_id'] = session_id[1]
                res = func(*args,**kwargs)
                return res
        else:
            send_dic = {'flag':False,'msg':'请先登录账号！'}
            print(send_dic)
            send_msg(send_dic,args[1])

    return inner