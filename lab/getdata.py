import baostock as bs
import pandas as pd
import csv


def readCsvFile():
    res = []
    with open('../codes.csv', 'r') as f:
        file = csv.reader(f)
        for line in file:
            res.append(line[0])
    return res


def produceData(code):
    # 获取A股历史数据 http://baostock.com/baostock/index.php/A%E8%82%A1K%E7%BA%BF%E6%95%B0%E6%8D%AE
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date='2000-01-01', end_date='',
                                      frequency="d", adjustflag="2")

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("../data/%s.csv" % code, index=False)


lg = bs.login()

codes = readCsvFile()

for index, row in enumerate(codes):
    produceData(row)

bs.logout()
