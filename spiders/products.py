import scrapy
import json


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['leclubleaderprice.fr']
    products = json.load(open("./output/product-links.json"))
    start_urls = [p['product_link'] for p in products]

    def parse(self, response):
        print(response.css('title::text').get().strip())
