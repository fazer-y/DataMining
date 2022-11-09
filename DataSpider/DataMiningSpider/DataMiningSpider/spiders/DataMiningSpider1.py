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
        print(urls)
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_url)
        
        print("正在爬取第" + str(count) + "页")


        if(count < 5000):
            nextUrl = "http://search.ndltd.org/search.php?q=%E5%9C%B0%E7%90%86&source_set_names=National+Digital+Library+of+Theses+and+Dissertations+in+Taiwan&year_start=2000&year_end=2022&start=" + \
                str(count * 10)
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def parse_url(self, response):
        # 创建一个item对象
        item = DataminingspiderItem()
        # 提取图片的每一个信息
        # 获取论文地址
        url = self.urlFront + response.xpath(
            '/html/body/div[2]/div/div[3]/ol/li[1]/a/text()').extract_first()
        print(url)
        # 请求下载论文信息页面
        yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        # 提取论文信息
        item = DataminingspiderItem()
        item['author'] = response.xpath('//*[@id="format0_disparea"]/tbody/tr[2]/td/a/text()').extract_first()
        item['title'] = response.xpath('//*[@id="format0_disparea"]/tbody/tr[4]/td/text()').extract_first()
        item['instructor'] = response.xpath('//*[@id="format0_disparea"]/tbody/tr[6]/td/a[1]/text()').extract_first()
        item['defenseMember'] = response.xpath('//*[@id="format0_disparea"]/tbody/tr[8]/td/a/text()').extract().join("、")

        yield item