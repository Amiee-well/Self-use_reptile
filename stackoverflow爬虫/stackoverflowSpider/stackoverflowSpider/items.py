# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StackoverflowspiderItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 问题链接
    question_link = scrapy.Field()
    # 投票数
    num_votes = scrapy.Field()
    # 回答数
    num_answers = scrapy.Field()
    # 查看数
    num_views = scrapy.Field()
    # tags
    tags = scrapy.Field()