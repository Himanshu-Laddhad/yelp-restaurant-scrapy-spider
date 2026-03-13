# yelp_scraper/pipelines.py
from itemadapter import ItemAdapter
import csv
from datetime import datetime

class YelpScraperPipeline:
    """
    Simple pipeline that ensures data consistency
    and can export to additional files if needed.
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Normalize fields
        adapter["name"] = (adapter.get("name") or "").strip()
        adapter["review_text"] = (adapter.get("review_text") or "").strip()

        return item
