# coding:utf-8

# 数据库信息
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'zhihu',
    'user': 'root',
    'password': '112358'
}

# 将新用户纳入user表的条件， 大于等于
New_User = {
    'agree': 1000,
    'answer': 1,
    'followers': 100
}

User_Agent= 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5' \
           '4.0.2840.99 Safari/537.36'