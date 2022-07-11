from typing import Optional
import scrapy
from scraper.items import ImageItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.imdb.com/title/tt4574334/episodes']

    EXPORT_FOLDER = 'exports/image'

    custom_settings: Optional[dict] = {
        'ITEM_PIPELINES': {
            'scrapy.pipelines.images.ImagesPipeline': 100,
        },
        'LOG_LEVEL': 'WARNING',
        'IMAGES_STORE': f'{EXPORT_FOLDER}/images',
    }

    def parse(self, response):       
        item = ImageItem()
        rel_urls = response.css('img::attr(src)').getall()
        abs_urls = [response.urljoin(url) for url in rel_urls]
        item['image_urls'] = abs_urls
        yield item
