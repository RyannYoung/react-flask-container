# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DynamicItem(scrapy.Item):
    address = scrapy.Field()
    phone = scrapy.Field()
    pass

class GenericItem(scrapy.Item):
    titles = scrapy.Field()
    heading_ones = scrapy.Field()
    heading_twos = scrapy.Field()
    heading_threes = scrapy.Field()
    tables = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    pass
