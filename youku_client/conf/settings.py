# Author:Cecilia
import os

# 客户端的总目录位置
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 管理员上传电影的电影目录路径
UPLOAD_PATH = os.path.join(BASE_PATH,'upload_movies')


# 用户下载电影存放目录
DOWNLOAD_PATH  = os.path.join(BASE_PATH,'download_movies')