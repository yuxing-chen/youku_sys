# Author:Cecilia


from db import user_data,models
from conf import settings
from lib import common
import os
import datetime


# 用户购买会员接口
@common.login_auth
def buy_vip_interface(back_dic,conn):
    user_obj = models.User.select(user_id = back_dic.get('user_id'))[0]
    # 判断该用户是否是会员
    if user_obj.is_vip:
        send_dic = {'flag':False,'msg':'你已经是vip了，不需要重复购买！'}
    else:
        user_obj.is_vip = 1
        user_obj.sql_update()
        send_dic = {'flag':True,'msg':'购买vip成功'}
    print(send_dic)
    common.send_msg(send_dic,conn)





# 用户下载免费电影电影接口
@common.login_auth
def download_free_movie_interface(back_dic,conn):
    movie_name = back_dic.get('movie_name')
    movie_path = os.path.join(settings.DOWNLOAD_PATH,movie_name)
    movie_size = os.path.getsize(movie_path)
    movie_path = os.path.join(settings.DOWNLOAD_PATH, movie_name)

    user_obj = models.User.select(user_id = back_dic.get('user_id'))[0]
    wait = 0
    # 判断用户是否为vip
    if not user_obj.is_vip:
        # 不是vip则需要等待广告时间
        wait = 5
        send_dic = {'flag': True, 'msg':'由于你不是vip用户，需要等待5秒广告时间','wait':wait,'movie_size':movie_size}
    else:
        send_dic = {'flag': True, 'msg':'由于是vip用户，不需要等待广告时间','wait':wait,'movie_size':movie_size}

    download_record_obj = models.DownLoadRecord(user_id=back_dic.get('user_id'),
                                                movie_id=back_dic.get('movie_id'),
                                                download_time=datetime.datetime.now())

    download_record_obj.save()

    print(send_dic)
    common.send_msg(send_dic,conn,movie_path)







# 用户下载收费电影功能
@common.login_auth
def download_nofree_movie_interface(back_dic,conn):
    movie_name = back_dic.get('movie_name')
    movie_path = os.path.join(settings.DOWNLOAD_PATH, movie_name)
    movie_size = os.path.getsize(movie_path)
    movie_path = os.path.join(settings.DOWNLOAD_PATH, movie_name)

    user_obj = models.User.select(user_id=back_dic.get('user_id'))[0]

    if not user_obj.is_vip:

        send_dic = {'flag': False, 'msg': '由于你不是vip用户,不能下载收费视频！'}
        print(send_dic)
        common.send_msg(send_dic, conn)
    else:
        send_dic = {'flag': True, 'msg': '由于是vip用户，不需要等待广告时间', 'movie_size': movie_size}

        download_record_obj = models.DownLoadRecord(user_id=back_dic.get('user_id'),
                                                    movie_id=back_dic.get('movie_id'),
                                                    download_time=datetime.datetime.now())

        download_record_obj.save()

        print(send_dic)
        common.send_msg(send_dic, conn, movie_path)






# 用户查看观影记录
@common.login_auth
def check_movie_record_interface(back_dic,conn):
    record_list = []
    record_obj_list = models.DownLoadRecord.select(user_id = back_dic.get('user_id'))
    if record_obj_list:
        for record_obj in record_obj_list:
            movie_obj = models.Movie.select(movie_id = record_obj.user_id)[0]
            record_list.append([movie_obj.movie_name,str(record_obj.download_time)])
        send_dic = {'flag':True,'record_list':record_list}


    else:
        send_dic = {'flag':False,'msg':'暂时没有任何观影记录！'}
    print(send_dic)
    common.send_msg(send_dic,conn)




# 用户查看公告
@common.login_auth
def check_notice_interface(back_dic,conn):
    notice_list = []

    notice_obj_list = models.Notice.select()
    if notice_obj_list:
        for notice_obj in notice_obj_list:
            notice_list.insert(0,[notice_obj.title,notice_obj.content,str(notice_obj.create_time)])
        send_dic = {'flag': True, 'notice_list': notice_list}


    else:
        send_dic = {'flag': False, 'msg': '暂时没有公告信息！'}
    print(send_dic)
    common.send_msg(send_dic, conn)








