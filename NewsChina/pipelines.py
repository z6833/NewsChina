# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from jieba import analyse
from openpyxl import Workbook
import pymysql

class KeyswordPipeline(object):
    """
    添加数据来源及抓取时间；
    结合textrank算法，抽取新闻中最重要的5个词，作为关键词
    """
    def process_item(self, item, spider):

        # 数据来源
        item['source'] = spider.name
        # 抓取时间
        item['utc_time'] = str(datetime.utcnow())

        content = item['content']
        keywords = ' '.join(analyse.textrank(content, topK=5))

        # 关键词
        item['keywords'] = keywords

        return item

class NewsChinaExcelPipeline(object):
    """
    数据保存
    """
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['标题', '关键词', '正文', '数据来源', '抓取时间'])

    def process_item(self, item, spider):

        data = [item['title'], item['keywords'], item['content'], item['source'], item['utc_time']]

        self.ws.append(data)
        self.wb.save('./news.xls')

        return item

# class NewschinaPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect(
#             host='.......',
#             port=3306,
#             database='news_China',
#             user='z',
#             password='136833',
#             charset='utf8'
#         )
#         # 实例一个游标
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         sql = """
#               insert into ChinaNews(ID, 标题, 关键词, 正文, 数据来源, 抓取时间)
#                values (%s, %s, %s, %s, %s, %s);"""
#
#         values = [
#             item['title'],
#             item['keywords'],
#             item['content'],
#
#             item['source'],
#             item['utc_time']
#         ]
#
#         self.cursor.execute(sql, values)
#         self.conn.commit()
#
#         return item
#
#     def close_spider(self, spider):
#         self.cursor.close()
#         self.conn.close()
