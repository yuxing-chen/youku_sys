# Author:Cecilia

from  lib import common
from db import models,user_data
import datetime


# 管理员/普通用户注册接口
def register_interface(back_dic,conn):
    user_name = back_dic.get('name')
    user_pwd = common.get_pwd_md5(back_dic.get('pwd'))
    user_type = back_dic.get('user_type')

    user_obj_list = models.User.select(user_name=user_name)
    if user_obj_list:
        for user_obj in user_obj_list:
            if user_obj.user_type == user_type:
                send_dic = {'flag':False,'msg':'该用户已经存在了！'}
                break

        else:
            user_obj = models.User(user_name=user_name,
                                   pwd=user_pwd,
                                   is_vip=0,
                                   is_locked=0,
                                   user_type=user_type,
                                   register_time=datetime.datetime.now())
            user_obj.save()
            send_dic = {'flag': True, 'msg': '用户注册成功'}




    else:
        user_obj = models.User(user_name = user_name,
                               pwd = user_pwd,
                               is_vip = 0,
                               is_locked = 0,
                               user_type = user_type,
                               register_time = datetime.datetime.now())
        user_obj.save()
        send_dic = {'flag':True,'msg':'用户注册成功'}

    print(send_dic)
    common.send_msg(send_dic, conn)





# 管理员/普通用户登录接口
def login_interface(back_dic,conn):
    user_name = back_dic.get('name')
    user_pwd = common.get_pwd_md5(back_dic.get('pwd'))
    user_type = back_dic.get('user_type')

    user_obj_list = models.User.select(user_name=user_name)
    if user_obj_list:
        for user_obj in user_obj_list:
            if user_obj.user_type == user_type:
                if user_obj.pwd == user_pwd:

                    session = common.get_session_md5(user_name)
                    addr = back_dic.get('addr')

                    user_data.metux.acquire()
                    user_data.online_user[addr] = [session,user_obj.user_id]
                    user_data.metux.release()

                    send_dic = {'flag':True,'msg':'用户登录成功！','session':session}
                else:
                    send_dic = {'flag': False, 'msg': '该用户密码错误！'}
                break

        else:
            send_dic = {'flag': False, 'msg': '该用户不存在！'}
    else:
        send_dic = {'flag': False, 'msg': '该用户不存在！'}

    print(send_dic)
    common.send_msg(send_dic,conn)






# 管理员上传电影经过的接口，判断管理员上传的电影是否存在
@common.login_auth
def check_movie_interface(back_dic,conn):
    movie_obj = models.Movie.select(file_md5 = back_dic.get('movie_md5'))
    if movie_obj:
        send_dic = {'flag':False,'msg':'电影已经存在了！'}

    else:
        send_dic = {'flag':True,'msg':'电影可以上传'}
    print(send_dic)
    common.send_msg(send_dic,conn)






# 获取电影的接口
# 管理员删除电影获取未删除的电影
# 用户下载免费电影获取免费视频
# 用户下载收费电影获取收费视频
@common.login_auth
def get_movie_list_interface(back_dic,conn):
    movie_type = back_dic.get('movie_type')
    movie_list = [] # 用来存储返回给客户端的电影列表
    check_movie_list = [] # 存储所有未删除的电影
    movie_obj_list = models.Movie.select()# 获取电影表中所有的电影

    # 判断电影表中是否有电影记录
    if movie_obj_list:
        # 循环所有的电影，获取所有的可删除电影
        for movie_obj in movie_obj_list:
            if not movie_obj.is_delete:
                check_movie_list.append(movie_obj)

        # 判断是否有可以删除的电影
        if check_movie_list:

            # 判断客户端传来的额获取电影的标识
            # 获取未删除的电影列表
            if movie_type == 'delete':
                for movie_obj in check_movie_list:
                    if not movie_obj.is_delete:
                       movie_list.append([movie_obj.movie_name,'免费' if movie_obj.is_free else '收费',movie_obj.movie_id])


            # 获取所有免费的电影列表
            if movie_type == 'free':
                for movie_obj in check_movie_list:
                    if  movie_obj.is_free:
                       movie_list.append([movie_obj.movie_name,'免费',movie_obj.movie_id])

            # 货物收费电影的列表
            if movie_type == 'nofree':
                for movie_obj in check_movie_list:
                    if not movie_obj.is_free:
                       movie_list.append([movie_obj.movie_name,'收费',movie_obj.movie_id])

            if movie_list:
                send_dic = {'flag':True,'movie_list':movie_list}
            else:
                send_dic = {'flag': False, 'msg': '没有电影！'}

        else:
            send_dic = {'flag': False, 'msg': '没有电影！'}

    else:
        send_dic = {'flag':False,'msg':'没有电影！'}

    print(send_dic)
    common.send_msg(send_dic,conn)






