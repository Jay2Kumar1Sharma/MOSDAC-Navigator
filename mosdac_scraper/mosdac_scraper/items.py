import scrapy

class MosdacItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    content_type = scrapy.Field()