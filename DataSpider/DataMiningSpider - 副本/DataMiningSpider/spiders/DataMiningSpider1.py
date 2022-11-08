import scrapy
from DataMiningSpider.items import DataminingspiderItem
count = 0

class Dataminingspider1Spider(scrapy.Spider):
    name = 'DataMiningSpider1'
    allowed_domains = ['search.ndltd.org']
    urlFront = "http://search.ndltd.org/"
    start_urls = ["http://search.ndltd.org/search.php?q=%E5%9C%B0%E7%90%86&source_set_names=National+Digital+Library+of+Theses+and+Dissertations+in+Taiwan&year_start=2000&year_end=2022"]

    def parse(self, response):
        global count
        count += 1
        urls = []
        urls = [(self.urlFront + url) for url in response.xpath(
            '//td[@class="search_table_detail_col"]/h4/a/@href').extract()]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
        print("正在爬取第" + str(count) + "页")


        if(count < 5000):
            nextUrl = "http://search.ndltd.org/search.php?q=%E5%9C%B0%E7%90%86&source_set_names=National+Digital+Library+of+Theses+and+Dissertations+in+Taiwan&year_start=2000&year_end=2022&start=" + \
                str(count * 10)
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def parse_detail(self, response):
        # 创建一个item对象
        item = DataminingspiderItem()
        # 提取图片的每一个信息
        # title
        item['detailUrl'] = response.xpath(
            '/html/body/div[2]/div/div[3]/ol/li[1]/a/text()').extract_first()
        item['title'] = response.xpath(
            '/html/body/div[2]/div/div[1]/h2/text()').extract_first()
        # 将item发送出去
        yield item