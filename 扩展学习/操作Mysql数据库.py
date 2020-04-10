import pymysql

# 第一步链接到数据库
coon = pymysql.connect(
    host="120.78.128.25",
    port=3306,
    user="future",
    password="123456",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
# 创建一个游标对象
cur = coon.cursor()
sql = "select * from futureloan.member LIMIT 10"
# 第三步：执行sql语句
res = cur.execute(sql)
print(res)

# 第四步：获取查询到的结果
# fetchone 获取查询到的一条数据
data = cur.fetchone()
print(data)
