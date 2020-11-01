import scrapy

from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def clean_description(value):
    return value.rstrip("...more")

def clean_price(value):
    return value.lstrip('£')

def define_thumbnail_absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)


class BookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    thumbnail = scrapy.Field(
        input_processor=MapCompose(define_thumbnail_absolute_url)
    )
    price = scrapy.item.Field(
        input_processor=MapCompose(clean_price, float)
    )
    stock = scrapy.Field(
        input_processor=MapCompose(int)
    )
    rate = scrapy.Field(
        input_processor=MapCompose(str.lower)
    )
    description = scrapy.Field(
        input_processor=MapCompose(clean_description, str.strip)
    )
    url = scrapy.Field()
