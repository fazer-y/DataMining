# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter


class GeogntuspiderPipeline:
    def __init__(self):
        self.f = open('urls.csv', 'w', encoding='utf-8',
                      newline='')       # line1
        self.file_name = ['期刊标题', '作者', '期数', '年代', '关键词']  # line2
        self.writer = csv.DictWriter(
            self.f, fieldnames=self.file_name)     # line3
        self.writer.writeheader()              # line4

    def process_item(self, item, spider):
        self.writer.writerow(
            {'期刊标题': item['title']
            ,'作者': item['author']
            ,'期数':item['order']
            ,'年代': item['dateOfPublication']
            ,'关键词': item['keyword']})
        return item  # line6

    def close_spider(self, spider):
        self.f.close()
