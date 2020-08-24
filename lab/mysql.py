import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123", "test")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# # 使用 execute() 方法执行 SQL，如果表存在则删除
# cursor.execute("drop table if exists daily_stock")

# # 使用预处理语句创建表
# sql = """create table daily_stock (
#         ts_code char(20) primary key not null,
#         trade_date char(20),
#         open float,
#         high float,
#         low float,
#         close float,
#         pre_close float,
#         `change` float,
#         pct_chg float,
#         vol float,
#         amount float )"""

# cursor.execute(sql)

data2 = ['000001.SZ', '20180718', 8.75,  8.85,  8.69,
         8.70, 8.72, -0.02, -0.23, 525152.77, 460697.377]

table = 'daily_stock'
values = ', '.join(['%s'] * len(data2))
sql3 = 'INSERT INTO {table} VALUES ({values})'.format(
    table=table, values=values)

try:
    # 执行sql语句
    # cursor.execute(sql2)
    cursor.execute(sql3, tuple(data2))
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()

# 关闭数据库连接
db.close()
