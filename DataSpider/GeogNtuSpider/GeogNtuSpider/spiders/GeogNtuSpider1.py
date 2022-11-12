import scrapy
from GeogNtuSpider.items import GeogntuspiderItem
count = 0
class GeogNtuSpiderSpider(scrapy.Spider):
    name = 'GeogNtuSpider1'
    
    domain = 'https://www.geog.ntu.edu.tw'
    allowed_domains = ['www.geog.ntu.edu.tw']
    start_urls = ['https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal1-20'
                ,'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal21-40'
                ,'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal41-60'
                ,'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal61-80'
                ,'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal78-100'
                ,'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal101-200']

    def parse(self, response):
        global count
        count += 1
        pages = [1, 20, 21, 40, 41, 60, 61, 80, 78, 100, 101, 200]
        pages = ['https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal1-20'
                , 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal21-40'
                , 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal41-60'
                , 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal61-80'                
                , 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal78-100'
                , 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal101-200']
        author = ""
        title = ""
        keywords = ""
        dateOfPublication = ""
        order = ""
        # 当前页面内所有子页地址
        urls = [self.domain + i for i in response.xpath(
            '//*[@id="adminForm"]/table/tfoot/tr/td/div/ul/li/a/@href').getall()[:-2]]
        # 'https://www.geog.ntu.edu.tw/index.php/tw/index.php/tw/journal/volumns/journal1-20?start=100'
        # 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal1-20?start=100'
        # 'https://www.geog.ntu.edu.tw/index.php/tw/journal/volumns/journal21-40?start=40'
        selectors = response.xpath(
            '//*[@id="t3-content"]/div/article/section/table/tbody/tr')
        if len(urls) != 0:
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_detail)
        elif response.xpath('//*[@id="t3-content"]/div/article/section/table/tbody/tr[1]/td[1]/strong/text()').get() == '類別':
            for i in range(0, len(selectors)):
                item = GeogntuspiderItem()
                author = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[3]/text()').get()
                title = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[2]/a/text()').get()
                keywords = "-"
                dateOfPublication = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[4]/text()').get()[1:]
                order = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[5]/text()').get()[1:]
                item['author'] = author
                item['title'] = title
                item['keyword'] = keywords
                item['dateOfPublication'] = dateOfPublication
                item['order'] = order
                yield item
        else:
            for i in range(0, len(selectors)):
                
                author = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[2]/text()').get()
                title = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[1]/a/text()').get()
                keywords = "-"
                dateOfPublication = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[3]/text()').get()[1:]
                order = response.xpath(
                    '//*[@id="t3-content"]/div/article/section/table/tbody/tr['+str(i+2)+']/td[4]/text()').get()[1:]
                item['author'] = author
                item['title'] = title
                item['keyword'] = keywords
                item['dateOfPublication'] = dateOfPublication
                item['order'] = order
                yield item

        # 下一页
        if count < 6:
            nextUrl = pages[count]
            print('\n___________________________________________________________')
            print(nextUrl)
            print('___________________________________________________________\n')
            yield scrapy.Request(url=nextUrl, callback=self.parse)


    # 解析子页内所有文章地址
    def parse_detail(self, response):
        urls = [self.domain + i for i in response.xpath(
            '//*[@id="adminForm"]/table/tbody/tr/td[1]/a/@href').getall()]
        for url in urls:
            url = url[:-3] + '0'
            yield scrapy.Request(url=url, callback=self.parse_detail_keyword)

    def parse_detail_keyword(self, response):
        author = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[3]/td[2]/text()').get()
        title = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[1]/td[2]/text()').get()
        keywords = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[8]/td[2]/text()').get()
        dateOfPublication = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[5]/td[2]/text()').get()
        order = response.xpath(
            '//*[@id="t3-content"]/table/tbody/tr[6]/td[2]/text()').get()
        item = GeogntuspiderItem()
        item['author'] = author
        item['title'] = title
        item['keyword'] = keywords
        item['dateOfPublication'] = dateOfPublication
        item['order'] = order
        yield item