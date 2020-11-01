from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

from .items import BookItem


class BookItemLoader(ItemLoader):
    default_item_class = BookItem
    default_output_processor = TakeFirst()
