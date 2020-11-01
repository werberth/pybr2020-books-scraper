import scrapy


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
        title = response.css(".product_main h1::text").get()
        thumbnail = response.css(".carousel-inner img::attr(src)").get()
        rate = response.css(".product_main .star-rating::attr(class)").get().split(' ')[-1]
        stock = response.css(".availability").re_first(r"(\d+)")
        description = response.css(".product_page > p::text").get()
        price = response.css(".product_main .price_color::text").get()
        return {
            "url": response.url,
            "title": title,
            "rate": rate,
            "stock": stock,
            "description": description,
            "price": price,
            "thumbnail": response.urljoin(image),
        }
