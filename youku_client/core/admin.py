# Author:Cecilia

from lib import common
from conf import settings
import os

# 管理员记录用户登录信息
user_info = {'cookies':None}



# 注册管理员用户
def register(client):
    while True:
        name = input('请输入管理员用户名:').strip()
        if name =='q':
            break
        pwd = input("请输入管理员密码:").strip()
        re_pwd = input('请确认密码:').strip()
        if re_pwd == pwd:
            # 两次密码一致，向服务端发送消息
            send_dic = {'type':'register',
                        'name':name,
                        'pwd':pwd,
                        'user_type':'admin'}
            back_dic =  common.send_msg(send_dic,client)
            # 接收服务端返会的消息
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
            else:
                print(back_dic.get('msg'))

        else:
            print('两次密码不一致！')


# 管理员用户登录
def login(client):
    while True:
        name = input('请输入管理员用户名:').strip()
        if name == 'q':
            break
        pwd = input("请输入管理员密码:").strip()

        # 向服务日发送消息
        send_dic = {'type': 'login',
                    'name': name,
                    'pwd': pwd,
                    'user_type': 'admin'}
        back_dic = common.send_msg(send_dic, client)
        if back_dic.get('flag'):
            print(back_dic.get('msg'))
            # 用户登录成功以后，服务器会将随机获取的唯一的加密字符串返回给用户，用户在用户端记录cookies值
            user_info['cookies'] = back_dic.get('session')
            break
        else:
            print(back_dic.get('msg'))






# 管理员上传电影功能
def upload_movie(client):
    while True:

        # 判断当前可以上传电影的文件夹是否存在
        if os.path.exists(settings.UPLOAD_PATH):
            movie_list = os.listdir(settings.UPLOAD_PATH)
            # 如存在，则获取电影列表，让管理员去上传的电影编号
            if movie_list:
                for i,movie in enumerate(movie_list):
                    print(f'{i}--{movie}')

                choice = input('请选择需要上传的电影编号:').strip()
                if choice == 'q':
                    break
                if not choice.isdigit():
                    print('必须是数字！')
                    continue
                choice = int(choice)
                if choice not in range(len(movie_list)):
                    print('输入错误！')
                    continue
                movie_name = movie_list[choice]
                movie_path = os.path.join(settings.UPLOAD_PATH,movie_name)

                # 选择电影编号，发送给服务端，判断电影是否存在，是否可以上传
                send_dic = {'type':'check_movie',
                            'session':user_info.get('cookies'),
                            'movie_name':movie_name,
                            # 获取电影的md5值，判断电影的数据准确性
                            'movie_md5':common.get_movie_md5(movie_path)}
                back_dic = common.send_msg(send_dic,client)

                # 接收服务端的相应信息，如可以上传，则选择改电影是否是免费
                if back_dic.get('flag'):
                    print(back_dic.get('msg'))

                    # 获取电影的大小
                    movie_size = os.path.getsize(movie_path)
                    is_free = input('是否免费(y:免费/n:收费):').strip()
                    if is_free !='y' and is_free !='Y' and is_free !='n' and is_free !='N':
                        print('输入错误！')
                        continue
                    # 将电影的一系列相关信息，一致发送给服务端
                    send_dic = {'type':'upload_movie',
                                'session':user_info.get('cookies'),
                                'movie_size':movie_size,
                                'movie_name': movie_name,
                                'movie_md5':common.get_movie_md5(movie_path),
                                'is_free':is_free}
                    print('电影正在上传。。。。。。。')
                    back_dic = common.send_msg(send_dic,client,movie_path)
                    if back_dic.get('flag'):
                        print(back_dic.get('msg'))
                        break
                    else:
                        print(back_dic.get('msg'))
                        break

                else:
                    print(back_dic.get('msg'))
                    break

            else:
                print('没有电影可以上传！')
                break

        else:
            print('没有电影可以上传！')
            break





# 管理员删除电影功能
def delete_movie(client):
    while True:
        # 先给服务端发送获取可以删除的电影列表
        send_dic = {'type':'get_movie_list',
                    'session':user_info.get('cookies'),
                    'movie_type':'delete'}

        back_dic = common.send_msg(send_dic,client)
        # 判断是否有可以删除的电影
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

            send_dic = {'type':'delete_movie',
                    'session':user_info.get('cookies'),
                        'movie_name':movie_name,
                        'movie_id':movie_id,
                        'movie_is_free':movie_is_free}
            print('电影正在删除。。。。。。')
            back_dic = common.send_msg(send_dic, client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
            else:
                print(back_dic.get('msg'))
                break
        else:
            print(back_dic.get('msg'))
            break





# 管理员发布公告功能
def send_notice(client):
    title = input('输入公告标题:').strip()
    content = input('输入公告内容:').strip()
    send_dic = {'type':'send_notice',
                'session':user_info.get('cookies'),
                'title':title,
                'content':content}
    back_dic = common.send_msg(send_dic,client)
    if back_dic.get('flag'):
        print(back_dic.get('msg'))
    else:
        print(back_dic.get('msg'))







func_dic = {
    '1':register,
    '2':login,
    '3':upload_movie,
    '4':delete_movie,
    '5':send_notice,
}
def admin_view(client):

    while True:
        print('''
        请选择功能:
        1.注册     2.登录     3.上传电影
        4.删除电影     5.发布公告     q.退出
        ''')
        choice = input('请输入功能编号:').strip()
        if choice == 'q':
            client.close()
            break
        if choice not in func_dic:
            print('没有这个功能！')
            continue

        func_dic.get(choice)(client)