# encoding = utf-8

from scrapy import cmdline

cmdline.execute('scrapy crawl newsChina'.split())

# import pymysql
#
# conn = pymysql.connect(
#             host='39.106.116.21',
#             port=3306,
#             database='news_China',
#             user='z',
#             password='136833',
#             charset='utf8'
# )
# cur = conn.cursor()
# sql = ("""CREATE TABLE IF NOT EXISTS ChinaNews(
#                                     ID INT PRIMARY KEY AUTO_INCREMENT,
#
#                                     标题 VARCHAR(40) DEFAULT "",
#                                     关键词 VARCHAR(40) DEFAULT "",
#                                     正文 VARCHAR(2000) DEFAULT "",
#
#                                     数据来源 VARCHAR(20) DEFAULT "",
#                                     抓取时间 DATETIME DEFAULT "1111-11-11"
#                 );
#
#                 """)
# cur.execute(sql)