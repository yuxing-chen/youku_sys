# Author:Cecilia

from tcp_client.client import get_client
from core import admin
from core import user


# 功能视图层，用于选择管理员视图和用户视图

func_dic = {
    '1':admin.admin_view,
    '2':user.user_view
}
def run():
    while True:
        print('''
        请选择功能:
        1.管理员功能     2.普通用户功能     q.退出
        ''')

        choice = input('请选择功能:').strip()
        if choice == 'q':
            break
        if choice not in func_dic:
            print('没有这个功能 ！')
            continue

        client = get_client()
        func_dic.get(choice)(client)
