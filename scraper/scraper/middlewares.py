# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from asyncio.windows_events import NULL
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.http import HtmlResponse
from scraper.utils.PlaywrightRequest import PlaywrightRequest
from playwright.sync_api import sync_playwright
from pywebcopy import save_webpage
from PIL import Image
import io

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class PlaywrightMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider
    
    def process_request(self, request, spider):
        if not isinstance(request, PlaywrightRequest):
            return None

        export_folder = request.export_folder

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_viewport_size({'width': 1920, 'height': 1080})
            page.goto(request.url)
            content = page.content()

            if(request.screenshot):
                request.meta['screenshot'] = page.screenshot(full_page=True)                

            if(request.pdf):
                page.emulate_media(media='screen')

                if(request.screenshot):
                    image = Image.open(io.BytesIO(request.meta['screenshot']))
                    print(f'width {image.width} height {image.height}')
                    request.meta['pdf'] = page.pdf(width=f"{image.width}px", height=f'{image.height}px', print_background=True)
                else:
                    request.meta['pdf'] = page.pdf(width="1920px", height="1080px")
        
            browser.close()
    
        return HtmlResponse(
            page.url,
            body=content,
            encoding="utf-8",
            request=request
        )
    
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
    
class ViewMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider
    
    def process_request(self, request, spider):

        print(request.url)

        if request.url.endswith('.txt'):
            return None

        save_webpage(
            url=request.url,
            project_folder="../exports/view",
            project_name="view",
            bypass_robots=True,
            open_in_browser=True,
            debug=True,
            threaded=False
        )

        return HtmlResponse(
            request.url,
            body=request.body,
            encoding="utf-8",
            request=request
        )

    def process_response(self, request, response, spider):
        print(response.url)
        return response
    
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
