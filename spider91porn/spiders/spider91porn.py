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
    allowed_domains = ["www.320lu.net/"]

    def start_requests(self):
        url = "http://www.320lu.net/vod-type-id-1-pg-{0}.html"
        for i in range(1, 10):
            yield scrapy.Request(url.format(i), callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//html/body/div[1]/div[4]/div/div[2]/div[2]/div/div[2]/ul/li/div/div'):
            # title = sel.xpath('h3/text()').extract()[0].strip()
            # link = "http://www.320lu.net"+ sel.xpath('@href').extract()[0]
            # movietime = sel.xpath('b/text()').extract()[0].strip("时长：")
            # upuser = sel.xpath('ul/li[2]/span/span[1]/text()').extract()[0].strip()
            # updatetime = sel.xpath('ul/li[2]/span/span[2]/text()').extract()[0].strip()
            # print(title, link, movietime, upuser, updatetime)
            item = Spider91PornItem()
            item['title'] = sel.xpath('a[1]/@title').extract()[0].strip('()')
            item['link'] = "http://www.320lu.net" + sel.xpath('a[1]/@href').extract()[0]
            item['movietime'] = sel.xpath('a[2]/b/text()').extract()[0].strip("时长：")
            item['upuser'] = sel.xpath('a[2]/ul/li[2]/span/span[1]/text()').extract()[0].strip()
            item['updatetime'] = sel.xpath('a[2]/ul/li/span/span[2]/text()').extract()[0].strip()
            urlpath = re.findall(r'.*2_(.*).jpg', sel.xpath('a/img/@data-original').extract()[0])[0]
            item['downurl'] = 'https://free5.qksdown.com/91porn/' + urlpath + '.mp4'
            m,s = item['movietime'].strip().split(":")
            movietime = int(m) * 60 + int(s)
            if movietime < 600:
                item['yesdown'] = 2
            else:
                item['yesdown'] = 1
            # yield scrapy.Request(url=item['downurl'], meta=item, callback=self.VideoDownload)
            yield item
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





























