# Author:Cecilia
import struct
import json
import os
import hashlib


# 客户端向服务端发送包头，数据，传输文件/接收数据
def send_msg(send_dic,client,file_path=None):
    json_data = json.dumps(send_dic).encode('utf8')
    headers = struct.pack('i', len(json_data))
    client.send(headers)
    client.send(json_data)

    if file_path:
        with open(file_path, 'rb') as fr:
            for line in fr:
                client.send(line)

    headers = client.recv(4)
    data_len = struct.unpack('i', headers)[0]
    json_data = client.recv(data_len)
    back_dic = json.loads(json_data.decode('utf8'))

    return back_dic





# 获取电影的md5值
def get_movie_md5(movie_path):
    movie_size = os.path.getsize(movie_path)
    md5 = hashlib.md5()
    md5_list = [0,movie_size//3,(movie_size//3)*2,movie_size-10]

    with open(movie_path,'rb') as fr:
        for md5_obj in md5_list:
            fr.seek(md5_obj)
            data = fr.read(10)
            md5.update(data)

    return md5.hexdigest()