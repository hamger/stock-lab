# coding:utf-8
import tushare as ts
import pandas as pd
from strategy import Strategy


class Lab(object):

    def __init__(self, args):
        self.strategyId = args.strategy if args.strategy else '1'

    def run(self):

        f = open("../token.txt")
        token = f.read()
        f.close()

        ts.set_token(token)
        pro = ts.pro_api()
        
        st = Strategy(pro)
        st.run(self.strategyId)
