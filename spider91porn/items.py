# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider91PornItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    upuser = scrapy.Field()
    updatetime = scrapy.Field()
    movietime = scrapy.Field()
    downurl = scrapy.Field()
    downstatus = scrapy.Field()
    fileurl = scrapy.Field()
    yesdown = scrapy.Field()
    video_local_path = scrapy.Field()

