import threading
import time


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
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

thread1 = Count("1", "counter_1", 1)
thread2 = Count("2", "counter_2", 2)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("主线程退出！")