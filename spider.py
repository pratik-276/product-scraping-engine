import scrapy

class ProductSpider(scrapy.Spider):
    name = 'productspider'
    start_urls = ['https://www.midsouthshooterssupply.com/dept/reloading/primers']

    def parse(self, response):
        products = []
        
        for product in response.css('.product'):
          dicty = {}
          dicty['price'] = float(str(product.css('.price-rating-container').css('.price').css('span').css('::text').get()).replace('$', ''))
          dicty['title'] = product.css('.product-description').css('.catalog-item-brand-item-number').css('.product-id').css('::text').get()
          dicty['stock'] = product.css('.price-rating-container').css('.status').css('span').css('::text').get() == 'In Stock'
          dicty['manufacturer'] = product.css('.product-description').css('.catalog-item-brand-item-number').css('.catalog-item-brand').css('::text').get()
          dicty['review'] = product.css('.catalog-item-name').css('::text').get()
          products.append(dicty)

        print("Products found are: ", products)

        if 'class' not in response.css('div.pagination').css('span').css('a')[-2].attrib:
            for href in [response.css('div.pagination').css('span').css('a')[-2]]:
                yield response.follow(href, self.parse)