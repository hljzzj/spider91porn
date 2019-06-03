import scrapy
from spider91porn.items import Spider91PornItem
from scrapy.loader.processors import MapCompose,Join
import re
import time
from os import path
import os
"""
scrapy crawl spider91porn -o 10.json
"""


class List91pornSpider(scrapy.Spider):
    name = "spider91porn"
    allowed_domains = ["http://www.320fff.com/"]
    domainurl = "http://www.320fff.com"  # 域名变更时修改此处

    def start_requests(self):
        url = self.domainurl + "/vod-type-id-1-pg-{0}.html"
        for i in range(1, 2):
            yield scrapy.Request(url.format(i), callback=self.parse)
# https://free3.qksdown.com/seporn/8fc8e4585c022520c1dd509ecfd09778/8fc8e4585c022520c1dd509ecfd09778.mp4?1554121681

    def parse(self, response):
        for sel in response.xpath('//*[@id="listcontent"]/div'):
            print('开始分析')
            print(sel.xpath('./div[1]/div/a/text()').extract()[0])
            # title = sel.xpath('//*[@id="listcontent"]/div[1]/div[1]/div/a/text()').extract()[0]
            # link = "http://www.320lu.net" + sel.xpath('//*[@id="listcontent"]/div[1]/div[1]/a/@href').extract()[0]
            # movietime = sel.xpath('//*[@id="listcontent"]/div[2]/div[1]/div/div/span/text()').extract()[0].strip("时长：")
            # upuser = sel.xpath('ul/li[2]/span/span[1]/text()').extract()[0].strip()
            # updatetime = sel.xpath('//*[@id="listcontent"]/div[2]/div[3]/div[1]/text()').extract()[0].strip('()')
            # print(title, link, movietime, updatetime)
            item = Spider91PornItem()
            item['title'] = sel.xpath('./div[1]/div/a/text()').extract()[0]
            item['link'] = self.domainurl + sel.xpath('div[1]/a/@href').extract()[0]
            item['movietime'] = sel.xpath('div[1]/div/div/span/text()').extract()[0].strip("时长：")
            # item['upuser'] = sel.xpath('a[2]/ul/li[2]/span/span[1]/text()').extract()[0].strip()
            item['updatetime'] = sel.xpath('div[3]/div[1]/text()').extract()[0].strip('()')
            urlpath = re.findall(r'.*1_(.*).jpg', sel.xpath('div[1]/a/img').extract()[0])[0]
            item['downurl'] = 'https://free5.qksdown.com/' + urlpath + '/' + urlpath + '.mp4'
            print('下载地址：')
            print('https://free5.qksdown.com/' + urlpath + '/' + urlpath + '.mp4')
            m, s = item['movietime'].strip().split(":")
            movietime = int(m) * 60 + int(s)
            if movietime < 480:
                item['yesdown'] = 2
            else:
                item['yesdown'] = 1
            # yield scrapy.Request(url=item['downurl'], meta=item, callback=self.VideoDownload)
            yield item
            print('分析完成')

    def VideoDownload(self, response):
        item = response.meta
        if item['movietime'] == '1':
            file_name = Join()([item['title'], '.mp4'])
            base_dir = path.join(path.curdir, 'VideoDownload')
            video_local_path = path.join(base_dir, file_name.replace('?', ''))
            item['video_local_path'] = video_local_path

            if not os.path.exists(base_dir):
                os.mkdir(base_dir)

            with open(video_local_path, "wb") as f:
                f.write(response.body)
        else:
            pass
        yield item
