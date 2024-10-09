import scrapy
from glamira_crawler.items import GlamiraCrawlerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class GlamiraSpider(CrawlSpider):
    name = 'glamira'
    allowed_domains = ['glamira.com']
    start_urls = ['https://www.glamira.com/jewelry/']  # Bắt đầu từ trang sản phẩm

    def parse(self, response):
        # Lấy link của từng sản phẩm
        product_links = response.css('a.product-item-link::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, self.parse_product)

        # Crawl qua các trang tiếp theo (pagination)
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        item = GlamiraCrawlerItem()
        
        # Lấy tên sản phẩm
        item['name'] = response.css('h1.page-title span::text').get()
        
        # Lấy giá sản phẩm
        item['price'] = response.css('span.price::text').get()

        # Lấy URL của ảnh
        item['image_urls'] = response.css('img.product-image-photo::attr(src)').getall()

        # Lấy mô tả sản phẩm
        item['description'] = response.css('div.product-info-main div.value::text').get()

        yield item
        pass
