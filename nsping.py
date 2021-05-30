# -*- coding=utf-8 -*-
# @Time: 2021/5/30 9:50
# @Author: 回梦
# @Cnblogs: https://www.lele8.me
import threading
import subprocess
import queue
import re
from datetime import *



def for_ping(Q):
    global num
    num = 0
    try:
        while True:
            if  Q.empty(): #队列为空时跳出循环
                break
            else:
                ip = Q.get()
                p = subprocess.Popen(["ping", "-n", "1", ip], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,shell=True) # ping一次，假如为linux平台可自行修改命令
                out = p.stdout.read().decode('gbk')
                matching = re.findall(r'TTL=[0-9].', out)
                nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
                if matching: #IP存活则输出或写入
                    print(ip)
                    num += 1
                    with open('{}.txt'.format(nowTime),'a',encoding='utf-8') as f:
                        f.write(ip+'\n')
                else:
                    pass

    except:
        pass

def get_ip():
    Q = queue.Queue()
    for d in range(0,256):
        for x in range(0,256):
            Q.put('10.{}.{}.1'.format(d,x)) #将循环的IP存入到队列
    threads = []
    for x in range(10): #根据个人需要进行更改，过大的话可能CPU直接100%
        th = threading.Thread(target=for_ping, args=(Q,))
        threads.append(th)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
if __name__ == '__main__':
    global num
    get_ip()
    print("共存活{}个网段".format(num))