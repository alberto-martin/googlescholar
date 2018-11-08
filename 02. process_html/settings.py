SPIDER_MODULES = ['scholar_scraper.spiders']
NEWSPIDER_MODULE = 'scholar_scraper.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
CONCURRENT_REQUESTS = 500
CONCURRENT_REQUESTS_PER_DOMAIN = 500
AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 30
COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us',
}


