import json
from urllib.request import urlretrieve
import urllib.request
import requests
from lxml import etree
import queue
import threading
import os
import time, datetime
from multiprocessing import Process,Pool
from tqdm import tqdm


class TqdmUpTo(tqdm):
    # Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    last_block = 0
    def update_to(self, block_num=1, block_size=1, total_size=None):
        '''
        block_num  : int, optional
            到目前为止传输的块 [default: 1].
        block_size : int, optional
            每个块的大小 (in tqdm units) [default: 1].
        total_size : int, optional
            文件总大小 (in tqdm units). 如果[default: None]保持不变.
        '''
        if total_size is not None:
            self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num

def Download(item):
    url = item['downurl']
    localpath = 'VideoDownload/'
    file_name = item['title']
    local = os.path.join(localpath, file_name + '.mp4.download')
    # print(url, localpath, file_name)
    try:
        #print('          开始下载 ' + file_name + '.mp4')
        #urlretrieve(url, local, Schedule)
        #urlretrieve(url, local)
        with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                      desc=file_name+'.mp4') as t:  # 继承至tqdm父类的初始化参数
            urlretrieve(url, filename=local, reporthook=t.update_to, data=None)
        os.rename(localpath + file_name + '.mp4.download', localpath + file_name + '.mp4')
        # print('  下载完成.' + file_name + '.mp4')
    except KeyboardInterrupt:
        print(file_name+'.mp4', '下载失败')
        t.close()
    t.close()


def Download2(item):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",}

    resp = requests.get(item['downurl'], headers=headers)
    localpath = 'VideoDownload/'

    local = os.path.join(localpath, file_name + '.mp4.download')
    print(local)
    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
        img_titles = item['title']
        img_urls = item['downurl']

        data = zip(img_titles, img_urls)
        for img_title, img_url in data:
            print('开始下载{title}.mp4'.format(title=img_title))
            result = urllib.request.urlretrieve(img_url, filename=local, reporthook=loading, data=None)
            print(result)
        os.rename(localpath + file_name + '.mp4.download', localpath + file_name + '.mp4')


def loading(blocknum,blocksize,totalsize):
    """
    回调函数: 数据传输时自动调用
    blocknum:已经传输的数据块数目
    blocksize:每个数据块字节
    totalsize:总字节
    """
    percent = int(100*blocknum*blocksize/totalsize)
    if percent > 100:
        percent = 100
    print("正在下载>>>{}%".format(percent))
    import time
    time.sleep(0.5)


def Download3(item):
    url = item['downurl']
    r = requests.get(url, stream=True)
    with open(item['title']+'.mp4.download', "wb") as mp4:
        for chunk in tqdm(r.iter_content()):
            if chunk:
                mp4.write(chunk)
        os.rename(item['title']+'.mp4.download', item['title']+'.mp4')
        print(item['title']+"  下载完成")


if __name__ == '__main__':
    localpath = 'VideoDownload/'

    local = os.path.join(localpath, '.mp4.download')
    print(local)
    with open("../10.json", 'r') as f:
        fileitem = json.loads(f.read())
        f.close()
    pool = Pool(processes=5)
    res_l = []
    for item in fileitem:
        if item['yesdown'] == 1:
            file_name = item['title']
            #print(item['downurl'])
            res = pool.apply_async(Download3, (item, ))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
            res_l.append(res)
            #print(item)
    pool.close()  # 关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束



