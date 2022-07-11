from typing import Optional
import scrapy
from scrapy.http.response.html import HtmlResponse
from scraper.items import GenericItem
from scraper.utils.Util import stripList

class GenericSpider(scrapy.Spider):
    name = 'generic'
    allowed_domains = ['google.com']
    start_urls = ['https://quotes.toscrape.com/tag/humor/']

    EXPORT_FOLDER = 'exports/generic'
    EXPORT_DATA = f'{EXPORT_FOLDER}/data'
    EXPORT_FILES = f'{EXPORT_FOLDER}/files'

    custom_settings: Optional[dict] = {
        'LOG_LEVEL': 'WARNING',
    }

    def parse(self, response: HtmlResponse):
        item = GenericItem()
        item['titles'] = stripList(response.css('title::text').getall())
        item['heading_ones'] = stripList(response.css('h1::text').getall())
        item['heading_twos'] = stripList(response.css('h2::text').getall())
        item['heading_threes'] = stripList(response.css('h3::text').getall())
        item['tables'] = stripList(response.css('table').getall())
        yield item    
