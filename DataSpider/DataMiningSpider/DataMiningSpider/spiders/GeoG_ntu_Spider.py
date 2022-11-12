import scrapy
from DataMiningSpider.items import GeogNtuSpiderItem


class GeogNtuSpiderSpider(scrapy.Spider):
    name = 'GeoG_ntu_Spider'
    conut = 1
    pages = [1, 20, 21, 40, 41, 60, 61, 77, 78, 100, 101, 200]
    urlFront = 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal'
    domain = 'https://www.geog.ntu.edu.tw/'
    allowed_domains = ['www.geog.ntu.edu.tw']
    start_urls = [
        'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal1-20']

    def parse(self, response):
        author = ""
        title = ""
        keywords = ""
        dateOfPublication = ""
        order = ""
        # 当前页面内所有子页地址
        urls = [self.domain + i for i in response.xpath(
            '//*[@id="adminForm"]/table/tfoot/tr/td/div/ul/li/a/@href').getall()[:-2]]

        if len(urls)!=0:
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_detail)
        else:
            selectors = response.xpath(
                '//*[@id="t3-content"]/div/article/section/table/tbody/tr')
            for i in range(0, len(selectors)):
                item = GeogNtuSpiderItem()
                author = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr[2]/td[2]/a/text()').get()
                title = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr[2]/td[1]/a/text()').get()
                keywords = ""
                dateOfPublication = response.xpath('//*[@id="t3-content"]/div/article/section/table/tbody/tr[2]/td[3]/text()').get()
                order = response.xpath('//*[@id="t3-content"]/div/article/section/table/tbody/tr[2]/td[4]/text()').get()
                item['author'] = author
                item['title'] = title
                item['keywords'] = keywords
                item['dateOfPublication'] = dateOfPublication
                item['order'] = order
                yield item

        # 下一页
        if self.count < 6:
            self.count += 1
            nextUrl=self.urlFront + \
                str(self.pages[self.conut*2]) + '-' + \
                    str(self.pages[self.conut*2])
            print('\n___________________________________________________________')
            print(nextUrl)
            print('___________________________________________________________\n')
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    # 解析子页内所有文章地址
    def parse_detail(self, response):
        urls = [ self.domain + i for i in response.xpath(
            '//*[@id="adminForm"]/table/tbody/tr/td[1]/a/@href').getall()]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail_keyword)

    def parse_detail_keyword(self, response):
        author = response.xpath('//*[@id="t3-content"]/table/tbody/tr[3]/td[2]/text()').get()
        title = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[1]/td[2]/text()').get()
        keywords = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[8]/td[2]/text()').get()
        dateOfPublication = response.xpath('//*[@id="t3-content"]/table/tbody/tr[5]/td[2]/text()').get()
        order = response.xpath('//*[@id="t3-content"]/table/tbody/tr[6]/td[2]/text()').get()
        item = GeogNtuSpiderItem()
        item['author'] = author
        item['title'] = title
        item['keywords'] = keywords
        item['dateOfPublication'] = dateOfPublication
        item['order'] = order

    def parse_detail_pdf(self, response):
        pass
