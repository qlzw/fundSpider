import threading
import time
import requests


class Count (threading.Thread):
    def __init__(self, threadId, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadId
        self.name = name
        self.delay = delay

    def run(self):
        print("线程：" + self.name + "开始！")
        print_time(self.name, self.delay, 5)
        print("线程：" + self.name + "结束！")


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# thread1 = Count("1", "counter_1", 1)
# thread2 = Count("2", "counter_2", 2)
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print("主线程退出！")

# url = "http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s6yzf;pn50;ddesc;qsd20200905;qed20210905;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"
# header = {
#     "Host": "fund.eastmoney.com",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Referer": "http://fund.eastmoney.com/HBJJ_pjsyl.html",
#     "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=08-10 19:52:23@#$%u5927%u6210%u9AD8%u65B0%u6280%u672F%u4EA7%u4E1A%u80A1%u7968A@%23%24000628; ASP.NET_SessionId=byju2k4rcgk5mvyzuduylxjp; qgqp_b_id=03bfaa04d18872f455dcd82c06f87769; st_si=53560516002141; st_asi=delete; MONITOR_WEB_ID=a4a1aa76-fab1-4a22-8eda-66536cdc5a8d; _adsame_fullscreen_16928=1; st_pvi=01694958318563; st_sp=2021-08-10%2019%3A52%3A24; st_inirUrl=https%3A%2F%2Fwww.google.com.hk%2F; st_sn=18; st_psi=20210905160057806-112200312936-2719885918",
#     "Connection": "keep-alive",
# }
# resp = requests.get(url, headers=header)
# content = resp.content.decode('utf-8')
# print(content)
# with open('data/fund.html', 'w') as f:
#     f.write(content)

# sc_map = {
#     '日增长率': 'rzdf',
#     '近1周': 'zzf',
#     '近1月': '1yzf',
#     '近3月': '3yzf',
#     '近6月': '6yzf',
#     '近1年': '1nzf',
#     '近2年': '2nzf',
#     '近3年': '3nzf',
#     '今年来': 'jnzf',
#     '成立以来': 'Inzf',
#     '自定义时间段':'qjzf'
#  }
# l = sc_map.values()
# print(type(l))
# for i  in l:
#     print(i)

list = [0, 1, 2, 3, 4, 5, 6]
print(list[1:3])