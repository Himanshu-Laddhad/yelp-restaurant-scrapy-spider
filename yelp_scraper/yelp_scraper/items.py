# yelp_scraper/items.py
import scrapy

class YelpScraperItem(scrapy.Item):
    # Basic restaurant info
    name = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    location = scrapy.Field()

    # Review-level fields
    reviewer_name = scrapy.Field()
    reviewer_rating = scrapy.Field()
    review_text = scrapy.Field()
