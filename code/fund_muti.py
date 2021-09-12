from datetime import date
from pandas.core import series
import requests
import json
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import time
import os
import threading
import fund
# url2 = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=6yzf&st=desc&sd=2020-09-05&ed=2021-09-05&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.011487374477119783"
# url3 = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-09-05&ed=2021-09-05&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.3770411775992588"


ft_map = {
    '全部': 'all',
    '股票型': 'gp',
    '混合型': 'hh',
    '债券型': 'zq',
    '指数型': 'zs',
    'QDII': 'qdii',
    'LOF': 'lof',
    'FOF': 'fof'
}
sc_map = {
    '日增长率': 'rzdf',
    '近1周': 'zzf',
    '近1月': '1yzf',
    '近3月': '3yzf',
    '近6月': '6yzf',
    '近1年': '1nzf',
    '近2年': '2nzf',
    '近3年': '3nzf',
    '今年来': 'jnzf',
    '成立以来': 'Inzf',
    '自定义时间段': 'qjzf'
}


class GetFundData(threading.Thread):
    def __init__(self, pageStart, pageEnd, dateStart, dateEnd, ft, sc, csv_path):
        threading.Thread.__init__(self)
        self.pageStart = pageStart
        self.pageEnd = pageEnd
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.ft = ft
        self.sc = sc
        self.csv_path = csv_path

    def run(self):
        get_fund_csv(self.pageStart, self.pageEnd, self.dateStart,
                     self.dateEnd, self.ft, self.sc, self.csv_path)


def get_fund_csv(pageStart, pageEnd, dateStart, dateEnd, ft, sc, csv_path):
    # sc按照哪个数据排序 ft按照哪个基金类型
    url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={ft}&rs=&gs=0&sc={sc}&st=desc&sd={sd}&ed={ed}&qdii=&tabSubtype=,,,,,&pi={page}&pn=50&dx=1&v=0.16911294275552802"
    header = {
        "Host": "fund.eastmoney.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "http://fund.eastmoney.com/HBJJ_pjsyl.html",
        "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=08-10 19:52:23@#$%u5927%u6210%u9AD8%u65B0%u6280%u672F%u4EA7%u4E1A%u80A1%u7968A@%23%24000628; ASP.NET_SessionId=byju2k4rcgk5mvyzuduylxjp; qgqp_b_id=03bfaa04d18872f455dcd82c06f87769; st_si=53560516002141; st_asi=delete; MONITOR_WEB_ID=a4a1aa76-fab1-4a22-8eda-66536cdc5a8d; _adsame_fullscreen_16928=1; st_pvi=01694958318563; st_sp=2021-08-10%2019%3A52%3A24; st_inirUrl=https%3A%2F%2Fwww.google.com.hk%2F; st_sn=18; st_psi=20210905160057806-112200312936-2719885918",
        "Connection": "keep-alive",
    }

    n = 0

    Data = np.zeros(((pageEnd - pageStart + 1)*50, 18)).astype(str)
    row = 50
    col = 18
    for page in range(pageStart, pageEnd+1):
        print("正在爬取第{}页".format(page))
        resp = requests.get(url.format(
            page=page, sd=dateStart, ed=dateEnd, ft=ft, sc=sc), timeout=30, headers=header)
        content = resp.content.decode('utf-8')

        # print(type(content))
        index1 = content.find("[")
        index2 = content.find("]")
        # print(content)
        content = content[index1:index2+1]
        data_json = json.loads(content)
        DD = np.zeros((row, col)).astype(str)

        for index, data in enumerate(data_json):
            dd = np.array(data.split(','))
            dd = [dd[0], dd[1], dd[3], dd[4], dd[5], dd[6], dd[7], dd[8], dd[9],
                  dd[10], dd[11], dd[12], dd[13], dd[14], dd[15], dd[16], dd[18], dd[19]]
            # print(dd)
            DD[index, :] = dd
        Data[n:n+50, :] = DD
        # print(Data)
        n += 50

    label = ["基金代码", "基金简称", "日期", "单位净值", "累计净值", "日增长率", "近1周", "近1月",
             "近3月", "近6月", "近1年", "近2年", "近3年", "今年来", "成立来", "成立时间", "{} 至 {}".format(dateStart, dateEnd), "手续费"]
    # print(data)
    df = DataFrame(Data, columns=label)
    df.to_csv(csv_path, index=False)


def thread_start(page, page_per_thread, dateStart, dateEnd, ft, sc, csv_file_name):
    # 全部基金最多174页
    if page > 174:
        page = 174
    if page < 0:
        print("page参数错误！")
        return
    start = 1
    end = start + page_per_thread - 1
    count = int(page/page_per_thread)
    suffix = '.csv'
    thread_list = []
    if page % page_per_thread != 0:
        count += 1
    for index in range(count):
        csv_path = csv_file_name + str(index) + suffix
        t = GetFundData(start, end, dateStart, dateEnd, ft, sc, csv_path)
        t.start()
        thread_list.append(t)
        start = end + 1
        if end < page:
            end = end + page_per_thread
        else:
            end = page
    return thread_list


if __name__ == '__main__':
    t1 = time.time()
    page_per_thread = 20
    page = 107
    csv_file_name = 'data/fund_data_muti'
    dateStart = '2021-02-01'
    dateEnd = '2021-09-11'
    sc = sc_map['近6月']
    ft = ft_map['全部']
    thread_list = thread_start(
        page, page_per_thread, dateStart, dateEnd, ft, sc, csv_file_name)
    for t in thread_list:
        t.join()
    t2 = time.time()
    print("总共消耗时间：{}s".format(t2 - t1))  # 21.901598930358887s
