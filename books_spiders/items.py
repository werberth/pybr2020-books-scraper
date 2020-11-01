import scrapy


class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    rate = scrapy.Field()
    stock = scrapy.Field()
