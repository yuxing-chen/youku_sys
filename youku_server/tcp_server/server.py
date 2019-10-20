# Author:Cecilia
import socket
import struct
import json
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(100)


from db import user_data
from interface import common_interface
from interface import admin_interface
from interface import user_interface
from lib import common







# 做任务分发的功能函数字典
func_dic = {
    'register':common_interface.register_interface,
    'login':common_interface.login_interface,
    'check_movie':common_interface.check_movie_interface,
    'upload_movie':admin_interface.upload_movie_interface,
    'get_movie_list':common_interface.get_movie_list_interface,
    'delete_movie':admin_interface.delete_movie_interface,
    'send_notice':admin_interface.send_notice_interface,
    'buy_vip':user_interface.buy_vip_interface,
    'download_free_movie':user_interface.download_free_movie_interface,
    'download_nofree_movie':user_interface.download_nofree_movie_interface,
    'check_movie_record':user_interface.check_movie_record_interface,
    'check_notice':user_interface.check_notice_interface,



}

# 服务端入口
def run():
    server = socket.socket()
    server.bind(('127.0.0.1',8007))
    server.listen(100)

    while True:
        conn,addr = server.accept()
        print(f'{addr}已经连接服务器')

        # 由线程池对象提交异步任务
        pool.submit(recv_work,conn,addr)



# 执行每个连接对象的请求操作
def recv_work(conn,addr):
    while True:
        try:
            # 接收数据头
            headers = conn.recv(4)
            data_len = struct.unpack('i',headers)[0]# 获取数据的总长度
            json_data = conn.recv(data_len) # 接收数据部分
            back_dic = json.loads(json_data.decode('utf8')) # 将数据反序列化
            back_dic['addr'] = addr

            # func是做任务分发工作的，将每个客户端的任务接收到，转去另一个地方执行
            func(back_dic,conn)
        except Exception as e:
            print(e)
            print(f'{addr}已经断开服务器连接了。。。。。。。')
            user_data.metux.acquire()
            user_data.online_user.pop(addr)
            user_data.metux.release()
            conn.close()
            break


# 任务分发函数
def func(back_dic,conn):
    if back_dic.get('type') not in func_dic:
        send_dic = {'flag':False,'msg':'请求错误！'}
        common.send_msg(send_dic,conn)

    else:
        print('进入',back_dic.get('type'))
        func_dic[back_dic.get('type')](back_dic,conn)
        print('结束',back_dic.get('type'))



