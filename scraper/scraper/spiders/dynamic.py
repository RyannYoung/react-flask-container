import os
from typing import Optional
import scrapy
from scraper.items import DynamicItem
from scrapy.http import HtmlResponse
from scraper.utils.PlaywrightRequest import PlaywrightRequest


class DynamicSpider(scrapy.Spider):
    name = 'dynamic'
    allowed_domains = ['google.com']
    start_urls = ['https://www.dunkindonuts.com/en/locations?location=02155']

    EXPORT_FOLDER = 'exports/dynamic'
    EXPORT_DATA = f'{EXPORT_FOLDER}/data'
    EXPORT_FILES = f'{EXPORT_FOLDER}/files'

    custom_settings: Optional[dict] = {
        'DOWNLOADER_MIDDLEWARES': {
            'scraper.middlewares.PlaywrightMiddleware': 100,
        },
        'LOG_LEVEL': 'INFO',
        'FEEDS': {
            f'{EXPORT_DATA}/dynamic.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
            },
            f'{EXPORT_DATA}/dynamic.json': {
                'format': 'json',
                'encoding': 'utf-8',
            },
            f'{EXPORT_DATA}/dynamic.jl': {
                'format': 'jsonlines',
                'encoding': 'utf-8',
            },
        },
    }

    def start_requests(self):
        for url in self.start_urls:
            yield PlaywrightRequest(
                url=url,
                screenshot=True,
                pdf=True
            )

    def parse(self, response: HtmlResponse):
        item = DynamicItem()
        
        # create a directory
        if not os.path.exists(self.EXPORT_FILES):
            os.mkdir(self.EXPORT_FILES)

        with open(f'{self.EXPORT_FILES}/image.png', 'wb') as file:
            file.write(response.meta['screenshot'])
            self.logger.info(f'Saved screenshot to {self.EXPORT_FILES}/image.png')
        
        with open(f'{self.EXPORT_FILES}/page.pdf', 'wb') as file:
            file.write(response.meta['pdf'])
            self.logger.info(f'Saved pdf to {self.EXPORT_FILES}/page.pdf')
        
        locations = response.css('li.store-item__wrapper')
        for location in locations:
            item['address'] = location.css('div div.store-item__address--line1 a::text').get()
            item['phone'] = location.css('span.js-store-phone::text').get()
            yield item
