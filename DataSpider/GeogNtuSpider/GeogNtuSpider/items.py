# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GeogntuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()             # 作者
    title = scrapy.Field()              # 论文标题
    keyword = scrapy.Field()            # 关键词
    dateOfPublication = scrapy.Field()  # 发表时间
    order = scrapy.Field()              # 期数
