# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from NewsChina.settings import USER_AGENTS as ua


class NewsChinaSpiderMiddleware(object):

    def process_request(self, request, spider):
        """
        给每一个请求随机分配一个代理
        :param request:
        :param spider:
        :return:
        """
        user_agent = random.choice(ua)
        request.headers['User-Agent'] = user_agent