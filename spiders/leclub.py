import scrapy


class LeclubSpider(scrapy.Spider):
    name = 'leclub'
    allowed_domains = ['leclubleaderprice.fr']
    start_urls = [
        'https://leclubleaderprice.fr/collections/bio',
        'https://leclubleaderprice.fr/collections/epicerie-salee',
        'https://leclubleaderprice.fr/collections/boissons',
        'https://leclubleaderprice.fr/collections/epicerie-sucree'
    ]

    def parse(self, response):
        for product in response.css("a.c-product-card__name"):
            url = response.urljoin(product.attrib['href'])
            yield {
                "product_name": product.css("a::text").get().strip(),
                "product_link": response.urljoin(product.attrib['href'])
            }

        max_page = response.css("div.c-load-more").attrib['data-max']
        for i in range(2,int(max_page)):
            href = response.urljoin("?page=" + str(i))
            yield response.follow(href, callback=self.parse)