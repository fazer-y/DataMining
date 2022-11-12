import scrapy
from DataMiningSpider.items import DataminingspiderItem
from urllib import parse
import requests
import re
count = 0


class Dataminingspider1Spider(scrapy.Spider):
    name = 'DataMiningSpider1'
    allowed_domains = ['search.ndltd.org', 'ndltd.ncl.edu.tw']
    urlFront = "http://search.ndltd.org/"
    start_urls = ["http://search.ndltd.org/search.php?q=%E5%9C%B0%E7%90%86&source_set_names=National+Digital+Library+of+Theses+and+Dissertations+in+Taiwan&year_start=2000&year_end=2022"]

    def parse(self, response):
        global count
        count += 1
        print("正在爬取第" + str(count) + "页")

        urls = []
        urls = [(self.urlFront + url) for url in response.xpath(
            '//td[@class="search_table_detail_col"]/h4/a/@href').extract()]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

        if(count < 2):
            nextUrl = "http://search.ndltd.org/search.php?q=%E5%9C%B0%E7%90%86&source_set_names=National+Digital+Library+of+Theses+and+Dissertations+in+Taiwan&year_start=2000&year_end=2022&start=" + \
                str(count * 10)
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def parse_url(self, response):
        
        # 获取论文地址
        url = response.xpath(
            '/html/body/div[2]/div/div[3]/ol/li[1]/a/text()').extract_first()
        # 请求下载论文信息页面
        yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        # 创建一个item对象
        # 提取论文信息
        item = DataminingspiderItem()
        title, defenseDate, degreeCategory, academic = \
            self.get_title(response.selector.xpath('//div[@id="aa"]')[0]
                .xpath('//table/tbody')[0]
                .xpath('//tr/td[@class="std2"]/text()').getall())
        
        author, instructor, defenseMember, nameOfTheAcademy, nameOfTheInstitute, keyWord = \
            self.get_author(response.selector.xpath('//div[@id="aa"]')[0]
                .xpath('//table/tbody')[0]
                .xpath('//tr/td[@headers="format_0_table"]/a/text()').getall())
        
        item['title'] = title
        item['defenseDate'] = defenseDate
        item['degreeCategory'] = degreeCategory
        item['academic'] = academic
        item['author'] = author
        item['instructor'] = instructor
        item['defenseMember'] = defenseMember
        item['nameOfTheAcademy'] = nameOfTheAcademy
        item['nameOfTheInstitute'] = nameOfTheInstitute
        item['keyWord'] = keyWord
        quot = response.selector.xpath('//div[@id="aa"]')[0]\
            .xpath('//table/tbody')[0].xpath('//tr/td[@class="std2"]/ul/li/text()').get()
        item['quotTimes'] = int(re.findall("\d+", quot)[0])
        yield item

    # def decode_utf8(self, s):
    #     s = s.encode('unicode_escape')
    #     ss = s.decode('utf-8').replace('\\x', '%')
    #     return parse.unquote(ss)

    def isalpha(self, s):
        if s > 'A' and s < 'Z' or s > 'a' and s < 'z':
            return True
        else:
            return False

    def get_author(self, selectors):
        c = 0
        length = len(selectors)
        author = selectors[0]
        c += 2

        instructor = ""
        for i in range(2, length):
            c += 1
            if self.isalpha(selectors[i][0]):
                continue
            else:
                if self.isalpha(selectors[i+1][0]):
                    instructor += selectors[i]
                    break
                else:
                    instructor += selectors[i] + "、"

        defenseMember = ""
        for i in range(c, length):
            c += 1
            if self.isalpha(selectors[i][0]):
                continue
            else:
                if self.isalpha(selectors[i+1][0]):
                    defenseMember += selectors[i]
                    break
                else:
                    defenseMember += selectors[i] + "、"

        for i in range(c, length):
            if self.isalpha(selectors[i][0]):
                c += 1
                continue
            else:
                break

        nameOfTheAcademy = selectors[c]
        c += 1
        nameOfTheInstitute = selectors[c]
        c += 1

        keyWord = ""
        for i in range(c, length):
            if self.isalpha(selectors[i+1][0]):
                keyWord += selectors[i]
                break
            else:
                keyWord += selectors[i] + "、"
        print(author, instructor, defenseMember,
              nameOfTheAcademy, nameOfTheInstitute, keyWord)
        return author, instructor, defenseMember, nameOfTheAcademy, nameOfTheInstitute, keyWord


    def get_title(self, selectors, sourcedata):
        title = ""
        defenseDate = ""
        degreeCategory = ""
        academic = ""

        title = selectors[1]
        c = 3
        for i in range(3, len(selectors)):
            if selectors[i] == '、':
                c += 1
                continue
            else:
                break
        defenseDate = selectors[c]
        degreeCategory = selectors[c+1]
        academic = selectors[c+3]
        print(title, defenseDate, degreeCategory, academic)
        return title, defenseDate, degreeCategory, academic
