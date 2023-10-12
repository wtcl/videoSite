import pymysql


# 连接数据库
conn = pymysql.connect(host = 'localhost',
                    port = 3306,
                    user = 'root',
                    passwd = '142536',
                    db = 'flask',
                    charset = 'utf8') # 获取连接

cursor = conn.cursor() # 获取游标

cursor.execute('SELECT * FROM user;')
# 查看一行 多行：cursor.fetchall()
row = cursor.fetchall()
print(row)