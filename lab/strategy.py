# coding:utf-8
import tushare as ts
import pandas as pd
import baostock as bs
from utils import readCsvFile


class Strategy(object):

    def __init__(self):
        self.data = readCsvFile('../codes.csv')

    def run(self, strategyId):
        bs.login()
        exec('self.strategy_%s()' % strategyId)
        bs.logout()

    def strategy_1(self):
        res = []
        for index, row in enumerate(self.data):
            # if index > 100:
            #     break

            rs = bs.query_history_k_data_plus(row,
                                              "date,code,open,high,low,close,preclose,pctChg,isST",
                                              start_date='2020-08-20', end_date='2020-08-24',
                                              frequency="d", adjustflag="2")

            tmp = []

            while (rs.error_code == '0') & rs.next():
                df = rs.get_row_data()
                if df[8] == 1:
                    continue
                # 条件1：当天为涨幅大于2%
                condition_1 = float(df[7]) >= 1
                # # 条件2：最大跌幅不超过1%
                # condition_2 = (float(df[2]) - float(df[4])) / float(df[2]) < 1 * 0.01
                # # 条件3：收盘价为最高价
                # condition_3 = float(df[5]) == float(df[3])
                if condition_1:
                    # if condition_1 and condition_2 and condition_3:
                    tmp.append(df[7])
            # 连续3天满足要求
            if len(tmp) >= 3:
                res.append(row)

        print(res)
