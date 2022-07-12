from scrapy import Request

class PlaywrightRequest(Request):
    def __init__(self, export_folder=None, screenshot=False, pdf=None, html=False, *args, **kwargs):
        self.screenshot = screenshot
        self.export_folder = export_folder
        self.pdf = pdf
        self.html = html
        super().__init__(*args, **kwargs)

