import json
from urllib.request import urlretrieve
import queue
import threading
import os
import time, datetime
from multiprocessing import Process,Pool


def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)
def Download(item):
    #print('gogogo')
    url = item['downurl']
    localpath = 'VideoDownload/'
    file_name = item['title']
    local = os.path.join(localpath, file_name + '.mp4')
    #print(url, localpath, file_name)
    try:
        # urlretrieve(url, local, Schedule)
        print('开始下载 ' + file_name + '.mp4')
        urlretrieve(url, local)
        print(file_name + '.mp4 下载完成.')
    except:
        print(file_name+'.mp4', '下载失败')



if __name__=='__main__':
    with open("../1.json", 'r') as f:
        fileitem = json.loads(f.read())
        f.close()
    pool = Pool(processes=10)
    res_l = []
    for item in fileitem[::-1]:
        if item['yesdown'] == 1:
            file_name = item['title']
            #print(item['downurl'])
            res = pool.apply_async(Download, (item, ))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
            res_l.append(res)
            #print(item)
    pool.close()  # 关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束



