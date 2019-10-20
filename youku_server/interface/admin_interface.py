# Author:Cecilia


from conf import settings
from lib import common
from db import models
from db import user_data
import  os
import datetime



# 管理员上传电影功能
@common.login_auth
def upload_movie_interface(back_doc,conn):
    # 获取用户传过来的字典的相关信息
    movie_md5 = back_doc.get('movie_md5')
    movie_size = back_doc.get('movie_size')
    is_free = back_doc.get('is_free')
    movie_name = back_doc.get('movie_name')

    # 先获取电影的名字，加密过后的
    movie_new_name = common.get_session_md5(movie_name)+movie_name
    # 获取电影的存放地址
    movie_path  = os.path.join(settings.DOWNLOAD_PATH,movie_new_name)

    recv_data = 0
    # 接收电影数据
    with open(movie_path,'wb') as fw:
        while recv_data < movie_size:
            data = conn.recv(1024)
            fw.write(data)
            recv_data += len(data)


    # 持久化存储到数据库
    movie_obj = models.Movie(movie_name = movie_new_name,
                             is_free = 1 if is_free=='Y'or is_free =='y' else 0,
                             is_delete = 0,
                             file_md5 = movie_md5,
                             path = movie_path,
                             upload_time = datetime.datetime.now(),
                             user_id = back_doc.get('user_id'))
    movie_obj.save()

    # 向客户端返回信息
    send_dic = {'flag':True,'msg':'电影上传成功'}
    common.send_msg(send_dic,conn)




# 管理员删除电影接口
@common.login_auth
def delete_movie_interface(back_dic,conn):
    movie_obj = models.Movie.select(movie_id = back_dic.get('movie_id'))[0]
    movie_obj.is_delete = 1
    movie_obj.sql_update()


    send_dic =  {'flag':True,'msg':'电影已经删除！'}
    print(send_dic)
    common.send_msg(send_dic,conn)



@common.login_auth
# 管理员发布公告信息接口
def send_notice_interface(back_dic,conn):
    notice_obj = models.Notice(title = back_dic.get('title'),
                               content  =back_dic.get('content'),
                               create_time  = datetime.datetime.now(),
                               user_id = back_dic.get('user_id'))
    notice_obj.save()

    send_dic = {'flag':True,'msg':'公告发布成功！'}
    print(send_dic)
    common.send_msg(send_dic,conn)


