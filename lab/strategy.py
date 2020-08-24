# coding:utf-8
import tushare as ts
import pandas as pd


class Strategy(object):

    def __init__(self, pro):
        self.pro = pro
        self.data = pro.query('stock_basic', exchange='', list_status='L',
                              fields='ts_code,symbol,name,area,industry,list_date')

        print('共统计' + str(len(self.data)) + '只上市股票。')

    def run(self, strategyId):
        exec('self.strategy_%s()'%strategyId)

    def strategy_1(self):
        pro = self.pro
        res = []
        for index, row in self.data.iterrows():
            if index > 1:
                break

            df = pro.query(
                'daily', ts_code=row["ts_code"], start_date='20200819', end_date='20200821')
            tmp = []
            for i, r in df.iterrows():
                # 条件1：当天为涨幅大于5%
                condition_1 = r['change'] / r['pre_close'] > 5 * 0.01
                # 条件2：最大跌幅不超过0.3%
                condition_2 = (r['pre_close'] - r['low']) / r['pre_close'] < 0.3 * 0.01
                if condition_1 and condition_2:
                    tmp.append(r['change'])
            if len(tmp) >= 3:
                res.append(row["ts_code"])

        print(res)
