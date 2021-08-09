import scrapy
from scrapy import Request
from datetime import date
from bs4 import BeautifulSoup




class WikiSpider(scrapy.Spider):
    name = 'Wiki'
    start_urls = ['https://en.wikipedia.org/wiki/Computer_simulation']
    #allowed_domains = ['en.wikipedia.org']

    def parse(self, response):
        for url in response.xpath('//div[@class="mw-parser-output"]/ul/li/a/@href'):
            href = response.urljoin(url.extract())
            yield Request(href, callback=self.parse_page)

    def parse_page(self, response):
        today = date.today()
        d = today.strftime("%d/%m/%Y")

        title = str(response.xpath('.//h1[@id ="firstHeading"]/text()').extract())
        data = str(response.css('ul').extract())
        txt = str(response.css('p').extract())



        item = {
            'date': d,
            'url': response.request.url,
            'title': BeautifulSoup(title).text,
            'data': BeautifulSoup(data).text,
            'text': BeautifulSoup(txt).text

        }
        yield item