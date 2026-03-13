# yelp_scraper/spiders/yelp_spider.py
import scrapy
import asyncio, random
from scrapy_playwright.page import PageMethod
from yelp_scraper.items import YelpScraperItem

class YelpSpider(scrapy.Spider):
    name = "yelp_spider"
    allowed_domains = ["yelp.com"]

    base_url = (
        "https://www.yelp.com/search?"
        "find_desc=Restaurants&find_loc=Indianapolis%2C+IN&start="
    )

    def start_requests(self):
        for i in range(0, 200, 10):  # 20 pages
            url = f"{self.base_url}{i}"
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_context": "default",
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", random.randint(2500, 4000)),
                    ],
                },
                callback=self.parse_listing,
            )

    async def parse_listing(self, response):
        listings = response.css("ul[class*='list__'] li div[class*='arrange__']")
        for card in listings:
            link = card.css("a.css-19v1rkv::attr(href)").get()
            if not link or not link.startswith("/biz/"):
                continue
            abs_link = response.urljoin(link)
            yield response.follow(
                abs_link,
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse_details,
            )
        await asyncio.sleep(random.uniform(1.5, 3.0))

    async def parse_details(self, response):
        item = YelpScraperItem()
        item["name"] = response.css("h1::text").get()
        item["rating"] = response.css("[aria-label*='star rating']::attr(aria-label)").get()
        item["num_reviews"] = response.css(".reviewCount__09f24__tnBk4::text").get()
        item["location"] = " ".join(response.css("address *::text").getall()).strip()
        item["tags"] = ", ".join(response.css("span.css-1p9ibgf::text").getall())
        item["link"] = response.url

        # --- Extract first-page reviews ---
        for review in response.css("div.review__09f24__oHr9V"):
            item["reviewer_name"] = review.css("a.css-1m051bw::text").get()
            item["reviewer_rating"] = review.css(
                "div[aria-label*='star rating']::attr(aria-label)"
            ).get()
            item["review_text"] = " ".join(review.css("span.raw__09f24__T4Ezm::text").getall())
            yield item

        await asyncio.sleep(random.uniform(1.0, 2.0))
