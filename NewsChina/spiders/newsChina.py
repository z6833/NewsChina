# -*- coding: utf-8 -*-
import re
import scrapy
from NewsChina.items import NewschinaItem

class NewschinaSpider(scrapy.Spider):
    name = 'newsChina'
    # allowed_domains = ['sou.chinanews.com']
    # start_urls = ['http://http://sou.chinanews.com/']

    #爬虫设置
    # handle_httpstatus_list = [403]  # 403错误时抛出异常
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RETRY_ENABLED": True,
    }

    page = 0
    # 提交参数
    formdata = {
        'field': 'content',
        'q': '滑坡 经济损失',
        'ps': '10',
        'start': '{}'.format(page * 10),
        'adv': '1',
        'time_scope': '0',
        'day1': '',
        'day2': '',
        'channel': 'gn',
        'creator': '',
        'sort': '_score'
    }
    # 提交url
    url = 'http://sou.chinanews.com/search.do'

    def start_requests(self):

        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.formdata,
            callback=self.parse
        )

    def parse(self, response):
        try:
            last_page = response.xpath('//div[@id="pagediv"]/span/text()').extract()[-1]
            # 匹配到尾页退出迭代
            if last_page is '尾页':
                return
        except:
            # 当匹配不到last_page时，说明已经爬取所有页面，xpath匹配失败
            # 抛出异常，这就是我们的循环终止条件
            # print("last_page:", response.url)
            return

        link_list = response.xpath('//div[@id="news_list"]/table//tr/td/ul/li/a/@href').extract()
        for link in link_list:
            if link:
                item = NewschinaItem()
                # 访问详情页
                yield scrapy.Request(link, callback=self.parse_detail, meta={'item': item})

        # 循环调用，访问下一页
        self.page += 1

        # 下一页的开始，修改该参数得到新数据
        self.formdata['start'] = '{}'.format(self.page * 10)
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.formdata,
            callback=self.parse
        )

    # 从详情页中解析数据
    def parse_detail(self, response):
        """
        分析发现，中新网年份不同，所以网页的表现形式不同，
        由于抓取的是所有的数据，因此同一个xpath可能只能匹配到部分的内容；
        经过反复测试发现提取规则只有如下几条。提取标题有两套规则
        提取正文有6套规则。
        :param response:
        :return:
        """
        item = response.meta['item']

        # 提取标题信息
        if response.xpath('//h1/text()'):
            item['title'] = response.xpath('//h1/text()').extract_first().strip()
        elif response.xpath('//title/text()'):
            item['title'] = response.xpath('//title/text()').extract_first().strip()
        else:
            print('title:', response.url)

        # 提取正文信息
        try:
            if response.xpath('//div[@id="ad0"]'):
                item['content'] = response.xpath('//div[@id="ad0"]').xpath('string(.)').extract_first().strip()
            elif response.xpath('//div[@class="left_zw"]'):
                item['content'] = response.xpath('//div[@class="left_zw"]').xpath('string(.)').extract_first().strip()
            elif response.xpath('//font[@id="Zoom"]'):
                item['content'] = response.xpath('//font[@id="Zoom"]').xpath('string(.)').extract_first().strip()
            elif response.xpath('//div[@id="qb"]'):
                item['content'] = response.xpath('//div[@id="qb"]').xpath('string(.)').extract_first().strip()
            elif response.xpath('//div[@class="video_con1_text_top"]/p'):
                item['content'] = response.xpath('//div[@class="video_con1_text_top"]/p').xpath('string(.)').extract_first().strip()
            else:
                print('content:', response.url)
        except:
            # 测试发现中新网有一个网页的链接是空的，因此提前不到正文，做异常处理
            print(response.url)
            item['content'] = ''

        yield item
