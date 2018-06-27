# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewschinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 数据来源
    source = scrapy.Field()
    # 抓取时间
    utc_time = scrapy.Field()

    # 新闻标题
    title = scrapy.Field()
    # 报导时间
    # reported = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
    # 关键词
    keywords = scrapy.Field()


