# Author:Cecilia

from lib import common
from conf import settings
import os,time

# 用户视图层


user_info = {'cookies':None}



# 注册用户功能
def register(client):
    while True:
        name = input('请输入用户名:').strip()
        if name =='q':
            break
        pwd = input("请输入密码:").strip()
        re_pwd = input('请确认密码:').strip()
        if re_pwd == pwd:
            # 两次密码一致，则向服务端发送信息进行是否可以注册用户
            send_dic = {'type':'register',
                        'name':name,
                        'pwd':pwd,
                        'user_type':'user'}
            back_dic =  common.send_msg(send_dic,client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
            else:
                print(back_dic.get('msg'))

        else:
            print('两次密码不一致！')



# 用户登录功能
def login(client):
    while True:
        name = input('请输入用户名:').strip()
        if name == 'q':
            break
        pwd = input("请输入用户密码:").strip()
        send_dic = {'type': 'login',
                    'name': name,
                    'pwd': pwd,
                    'user_type': 'user'}
        back_dic = common.send_msg(send_dic, client)
        if back_dic.get('flag'):
            print(back_dic.get('msg'))
            user_info['cookies'] = back_dic.get('session')
            break
        else:
            print(back_dic.get('msg'))







# 用户购买Vip功能
def buy_vip(client):
    while True:
        is_vip = input('是否购买vip(y:购买/不购买):').strip()
        if is_vip != 'y' and is_vip != 'Y':
            print('你放弃了购买vip！')
            break

        send_dic = {'type':'buy_vip',
                    'session':user_info.get('cookies'),
                    }
        back_dic = common.send_msg(send_dic, client)
        if back_dic.get('flag'):
            print(back_dic.get('msg'))
            break
        else:
            print(back_dic.get('msg'))
            break







# 用户查看电影功能
def check_movie(client):
    while True:
        send_dic = {'type':'get_movie_list',
                    'session':user_info.get('cookies'),
                    'movie_type':'delete'}

        back_dic = common.send_msg(send_dic,client)
        if back_dic.get('flag'):
            movie_list = back_dic.get('movie_list')
            for i, movie in enumerate(movie_list):
                print(f'{i}--{movie}')
            break
        else:
            print(back_dic.get('msg'))
            break




# 用户下载免费电影功能
def download_free_movie(client):
    while True:
        # 先向服务端获取免费的电影
        send_dic = {'type':'get_movie_list',
                    'session':user_info.get('cookies'),
                    'movie_type':'free'}

        back_dic = common.send_msg(send_dic,client)
        # 判断是否有免费电影可以下载
        if back_dic.get('flag'):
            movie_list = back_dic.get('movie_list')
            for i, movie in enumerate(movie_list):
                print(f'{i}--{movie}')

            choice = input('请选择需要下载的的电影编号:').strip()
            if choice == 'q':
                break
            if not choice.isdigit():
                print('必须是数字！')
                continue
            choice = int(choice)
            if choice not in range(len(movie_list)):
                print('输入错误！')
                continue

            movie_name,movie_is_free,movie_id = movie_list[choice]

            # 用户选择为需要下载的电影编号，发送给服务端
            send_dic = {'type':'download_free_movie',
                    'session':user_info.get('cookies'),
                        'movie_name':movie_name,
                        'movie_id':movie_id,
                        'movie_is_free':movie_is_free}
            back_dic = common.send_msg(send_dic, client)
            if back_dic.get('flag'):
                movie_path = os.path.join(settings.DOWNLOAD_PATH,movie_name)
                movie_size = back_dic.get('movie_size')
                print(back_dic.get('msg'))
                time.sleep(back_dic.get('wait'))
                print('电影开始下载。。。。。。')

                recv_data = 0
                with open(movie_path, 'wb') as fw:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        fw.write(data)
                        recv_data += len(data)
                print('电影下载成功')
                break
            else:
                print(back_dic.get('msg'))
                break
        else:
            print(back_dic.get('msg'))
            break








# 用户下载收费电影
def download_nofree_movie(client):
    while True:
        send_dic = {'type':'get_movie_list',
                    'session':user_info.get('cookies'),
                    'movie_type':'nofree'}

        back_dic = common.send_msg(send_dic,client)
        if back_dic.get('flag'):
            movie_list = back_dic.get('movie_list')
            for i, movie in enumerate(movie_list):
                print(f'{i}--{movie}')

            choice = input('请选择需要删除的的电影编号:').strip()
            if choice == 'q':
                break
            if not choice.isdigit():
                print('必须是数字！')
                continue
            choice = int(choice)
            if choice not in range(len(movie_list)):
                print('输入错误！')
                continue

            movie_name,movie_is_free,movie_id = movie_list[choice]
            send_dic = {'type':'download_nofree_movie',
                    'session':user_info.get('cookies'),
                        'movie_name':movie_name,
                        'movie_id':movie_id,
                        'movie_is_free':movie_is_free}
            back_dic = common.send_msg(send_dic, client)
            if back_dic.get('flag'):
                movie_path = os.path.join(settings.DOWNLOAD_PATH,movie_name)
                movie_size = back_dic.get('movie_size')
                print(back_dic.get('msg'))

                recv_data = 0
                with open(movie_path, 'wb') as fw:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        fw.write(data)
                        recv_data += len(data)
                print('电影下载成功')
                break
            else:
                print(back_dic.get('msg'))
                break
        else:
            print(back_dic.get('msg'))
            break






# 用户查看观影记录
def check_movie_record(client):
    send_dic = {'type':'check_movie_record',
                'session':user_info.get('cookies')
                }

    back_dic = common.send_msg(send_dic,client)
    if back_dic.get('flag'):
        record_list = back_dic.get('record_list')
        for i,record in enumerate(record_list):
            print(f'{i}---{record}')
    else:
        print(back_dic.get('msg'))


# 用户查看电影公告
def check_notice(client):
    send_dic = {'type': 'check_notice',
                'session': user_info.get('cookies')
                }

    back_dic = common.send_msg(send_dic, client)
    if back_dic.get('flag'):
        notice_list = back_dic.get('notice_list')
        for i, notice in enumerate(notice_list):
            print(f'{i}---{notice}')
    else:
        print(back_dic.get('msg'))





func_dic = {
    '1':register,
    '2':login,
    '3':buy_vip,
    '4':check_movie,
    '5':download_free_movie,
    '6':download_nofree_movie,
    '7':check_movie_record,
    '8':check_notice,
}
def user_view(client):
    while True:
        print('''
        请选择功能:
        1.注册          5.下载免费视频
        2.登录          6.下载收费视频
        3.冲会员         7.查看观影记录
        4.查看视频       8.查看公告
        q.退出
        ''')
        choice = input('请输入功能编号:').strip()
        if choice == 'q':
            client.close()
            break
        if choice not in func_dic:
            print('没有这个功能！')
            continue

        func_dic.get(choice)(client)