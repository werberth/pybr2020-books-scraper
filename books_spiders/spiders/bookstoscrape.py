import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..loader import BookItemLoader


class BookstoscrapeSpider(CrawlSpider):
    name = 'bookstoscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    category_lx = LinkExtractor(
        allow=r'catalogue/category/',
        restrict_css=".nav-list ul"
    )

    product_lx = LinkExtractor(
        allow=r'catalogue/[\w\-_]+/index.html',
        restrict_css=".product_pod h3"
    )

    rules = [
        Rule(category_lx),
        Rule(product_lx, callback='parse_book')
    ]

    def parse_book(self, response):
        loader = BookItemLoader(response=response)
        loader.add_css("title", ".product_main h1::text")
        loader.add_css("thumbnail", ".carousel-inner img::attr(src)")
        loader.add_css("description", ".product_page > p::text")
        loader.add_css("price", ".product_main .price_color::text")

        rate_css = ".product_main .star-rating::attr(class)"
        loader.add_value("rate",  response.css(rate_css).get().split(' ')[-1])

        loader.add_value("stock",
                         response.css(".availability").re_first(r"(\d+)"))
        loader.add_value("url", response.url)
        return loader.load_item()
