# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class DataminingspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    author = scrapy.Field()             # 作者
    title = scrapy.Field()              # 论文标题
    instructor = scrapy.Field()         # 导师
    defenseMember = scrapy.Field()      # 答辩委员
    defenseDate = scrapy.Field()        # 答辩日期
    degreeCategory = scrapy.Field()     # 学位类别
    nameOfTheAcademy = scrapy.Field()   # 院校名称 
    nameOfTheInstitute = scrapy.Field() # 系所名称
    academic = scrapy.Field()           # 学类
    summary = scrapy.Field()            # 摘要
    references = scrapy.Field()         # 参考文献
    keyWord = scrapy.Field()            # 关键词
    quotTimes = scrapy.Field()          # 被引用次数