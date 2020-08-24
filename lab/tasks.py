# Python实用宝典
# https://pythondict.com

import pymongo
import time
import json
import tushare as ts
from celery import Celery
import pymysql

# tushare
pro = ts.pro_api(
    token="574543edce877c61472d1e83e241142cca9d53865e5681180462cc7d")

# 打开数据库连接
db = pymysql.connect("localhost", "root", "", "test")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 新建celery任务
app = Celery('my_task')

@app.task
def get_stock_daily(start_date, end_date, code):
    """
    Celery任务：获得某股票的日线行情数据

    Args:
        start_date (str): 起始日
        end_date (str): 结束日
        code (str): 股票代码
    """

   # 请求tushare数据，并转化为json格式
    try:
        df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    except Exception as e:
        # 触发普通用户CPS限制，60秒后重试
        print(e)
        get_stock_daily.retry(countdown=60)

    data = json.loads(df.T.to_json()).values()
    print(data)
    # 对股票每一天数据进行保存，注意唯一性
    # 这里也可以批量创建，速度更快，但批量创建容易丢失数据
    # 这里为了保证数据的绝对稳定性，选择一条条创建
    for row in data:
        data2 = row.values
        values = ', '.join(['%s'] * len(data2))
        sql3 = 'INSERT INTO daily_stock VALUES ({values})'.format(values=values)
        try:
            # 执行sql语句
            cursor.execute(sql3, tuple(data2))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        # daily.update({"_id": f"{row['ts_code']}-{row['trade_date']}"}, row, upsert=True)

    print(f"{code}: 插入\更新 完毕 - {start_date} to {end_date}")
    # 关闭数据库连接
    db.close()
