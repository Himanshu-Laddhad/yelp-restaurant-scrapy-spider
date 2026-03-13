# yelp_scraper/settings.py
import os

BOT_NAME = "yelp_scraper"
SPIDER_MODULES = ["yelp_scraper.spiders"]
NEWSPIDER_MODULE = "yelp_scraper.spiders"

# ====================================================
# 🎭 Playwright Core
# ====================================================
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": [
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--no-sandbox",
        "--disable-gpu",
        "--start-maximized",
    ],
}

PLAYWRIGHT_CONTEXTS = {
    "default": {
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        ),
        "locale": "en-US",
        "color_scheme": "light",
        "permissions": ["geolocation"],
        "ignore_https_errors": True,
    }
}

# ====================================================
# ⚡ Scrapy Core
# ====================================================
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 3
DOWNLOAD_TIMEOUT = 120
LOG_LEVEL = "INFO"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    "yelp_indianapolis.csv": {"format": "csv", "overwrite": True},
}

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_MAX_DELAY = 10.0
DOWNLOAD_DELAY = 1.0
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 90000

# ====================================================
# 🔒 Zyte Smart Proxy Integration
# ====================================================
ZYTE_SMARTPROXY_ENABLED = True
ZYTE_SMARTPROXY_APIKEY = "ca4b10259bf344cba773085196460cc7"
ZYTE_SMARTPROXY_URL = "http://proxy.crawlera.com:8011"


DOWNLOADER_MIDDLEWARES = {
    "scrapy_playwright.middleware.PlaywrightMiddleware": 800,
    "scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware": 610,
}

RETRY_ENABLED = True
RETRY_TIMES = 3
DOWNLOAD_TIMEOUT = 180
