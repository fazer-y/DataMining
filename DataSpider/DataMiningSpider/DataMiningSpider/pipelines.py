# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class DataminingspiderPipeline:
    def __init__(self):
        self.f = open('urls.csv', 'w', encoding='utf-8',
                      newline='')       # line1
        self.file_name = ['detailUrl', 'title']  # line2
        self.writer = csv.DictWriter(
            self.f, fieldnames=self.file_name)     # line3
        self.writer.writeheader()              # line4

    def process_item(self, item, spider):
        self.writer.writerow(dict(item))              # line5
        return item  # line6

    def close_spider(self, spider):
        self.f.close()
