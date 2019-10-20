# Author:Cecilia
import socket


# 获取客户端连接对象
def get_client():
    client = socket.socket()
    client.connect(('127.0.0.1',8007))

    return client
