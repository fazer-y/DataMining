import scrapy

class dataSpider(scrapy.Spider):
    name = "dataSpider1"

    def start_requests(self):
        urls = [
            'https://hdl.handle.net/11296/4t6578',
            ''
        ]
        return super().start_requests()