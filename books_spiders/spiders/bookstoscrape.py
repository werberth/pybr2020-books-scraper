import scrapy

from scrapy.loader import ItemLoader

from ..loader import BookItemLoader


class BookstoscrapeSpider(scrapy.Spider):
    name = 'bookstoscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for path in response.css(".nav-list ul a::attr(href)").getall():
            yield scrapy.Request(response.urljoin(path),
                                 callback=self.parse_category)

    def parse_category(self, response):
        for path in response.css(".product_pod h3 a::attr(href)").getall():
            yield scrapy.Request(response.urljoin(path),
                                 callback=self.parse_book)

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
