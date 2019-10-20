# Author:Cecilia



from orm.orm_demo import Models,Integer,String

# 所有表类
# 用户表
class User(Models):
    # 自定义表名
    table_name = 'user_info'
    # 表字段
    user_id = Integer(name='user_id',primary_key=True)
    user_name = String(name='user_name')
    pwd = String(name='pwd')
    is_vip = Integer(name='is_vip')
    is_locked = Integer(name='is_locked')
    user_type = String(name='user_type')
    register_time = String(name='register_time')



# 电影表
class Movie(Models):
    # 自定义表名
    table_name = 'movie'
    # 表字段
    movie_id = Integer(name='movie_id',primary_key=True)
    movie_name = String(name='movie_name')
    is_free = Integer(name='is_free')
    is_delete = Integer(name='is_delete')
    file_md5 = String(name='file_md5')
    path = String(name='path')
    upload_time = String(name='upload_time')
    user_id = Integer(name='user_id')


# 公告表
class Notice(Models):
    # 自定义表名
    table_name = 'notice'
    # 表字段
    n_id = Integer(name='n_id',primary_key=True)
    title = String(name='title')
    content = String(name='content')
    create_time = String(name='create_time')
    user_id = Integer(name='user_id')



# 下载记录表
class DownLoadRecord(Models):
    # 自定义表名
    table_name = 'download_record'
    # 表字段
    download_id = Integer(name='download_id',primary_key=True)
    user_id = Integer(name='user_id')
    movie_id =Integer(name='movie_id')
    download_time = String(name='download_time')

