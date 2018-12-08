import json
from urllib.request import urlretrieve
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
    #print(url, localpath, file_name)
    try:
        #print('          开始下载 ' + file_name + '.mp4')
        #urlretrieve(url, local, Schedule)
        #urlretrieve(url, local)
        with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                      desc=file_name+'.mp4') as t:  # 继承至tqdm父类的初始化参数
            urlretrieve(url, filename=local, reporthook=t.update_to, data=None)
        os.rename(localpath + file_name +'.mp4.download',localpath + file_name + '.mp4')
        #print('  下载完成.' + file_name + '.mp4')
    except KeyboardInterrupt:
        print(file_name+'.mp4', '下载失败')
        t.close()
    t.close()



if __name__=='__main__':
    with open("../10.json", 'r') as f:
        fileitem = json.loads(f.read())
        f.close()
    pool = Pool(processes=5)
    res_l = []
    for item in fileitem:
        if item['yesdown'] == 1:
            file_name = item['title']
            #print(item['downurl'])
            res = pool.apply_async(Download, (item, ))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
            res_l.append(res)
            #print(item)
    pool.close()  # 关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束



