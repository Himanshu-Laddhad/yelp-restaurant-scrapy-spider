# HW7 – Yelp Indianapolis Restaurant Scraper (Scrapy + Playwright)

**Course:** MGTA 590 – Web Data Analytics | Purdue University
**Skills:** Python · Scrapy · Playwright · Async Scraping · CSS Selectors · Two-Level Crawling · Items Pipeline

---

## Overview

This project is a two-stage Scrapy spider that collects restaurant data and customer reviews from Yelp for **Indianapolis, IN**. Because Yelp heavily relies on JavaScript for rendering its search results and business pages, **scrapy-playwright** drives a headless Chromium browser to load each page before extraction.

The spider first scrapes restaurant listings across 20 search pages, then follows each restaurant's detail link to extract full business information and individual reviews — producing a rich, review-level dataset.

---

## What It Does

### Stage 1 – Listing Pages (20 pages × 10 results)
1. Generates paginated Yelp search URLs (`start=0` to `start=190`)
2. Launches Playwright, scrolls to trigger lazy-loaded content, waits for full render
3. Extracts restaurant detail page links from listing cards
4. Follows each link to Stage 2

### Stage 2 – Business Detail & Reviews
For each restaurant page, extracts:
- Restaurant name
- Star rating
- Review count
- Address / location
- Category tags
- For each review on the first page:
  - Reviewer name
  - Reviewer rating
  - Review text

---

## Project Structure

```
yelp_scraper/
├── scrapy.cfg
└── yelp_scraper/
    ├── __init__.py
    ├── items.py          # YelpScraperItem schema
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        └── yelp_spider.py  # Main spider (two-stage)
yelp_indianapolis.csv       # Output dataset
```

---

## Output Schema

```
name, rating, num_reviews, location, categories, link,
reviewer_name, reviewer_rating, review_text
```

---

## Sample Data

| Name | Rating | Reviews | Location | Categories |
|---|---|---|---|---|
| Shapiro's Delicatessen | 4.0 | 1071 | Pogue's Run | Sandwiches; Desserts; Delis |
| Firehouse Subs | 2.9 | 68 | — | Delis; Sandwiches; Fast Food |

---

## Key Concepts Demonstrated

| Concept | Description |
|---|---|
| Two-level Scrapy crawl | Listing → Detail page architecture |
| Playwright integration | Headless browser with scroll + wait actions |
| Random delays (`asyncio.sleep`) | Human-like timing between requests |
| CSS selectors | Extracting nested elements from dynamic DOM |
| Scrapy Items | Structured data schema with `YelpScraperItem` |
| `response.follow()` | Clean relative URL resolution |
| `PageMethod` | Injecting Playwright actions (scroll, wait) per request |

---

## Tech Stack

- **Language:** Python 3
- **Framework:** Scrapy
- **Browser Automation:** scrapy-playwright (Chromium)
- **Output:** CSV (via Scrapy FEEDS or pipeline)

---

## Prerequisites

```bash
pip install scrapy scrapy-playwright
playwright install chromium
```

---

## How to Run

```bash
cd yelp_scraper
scrapy crawl yelp_spider -o yelp_indianapolis.csv
```

---

## Configuration Notes

- The spider scrapes **20 listing pages** (200 restaurant cards) by default. Adjust the range in `start_requests()`:

  ```python
  for i in range(0, 200, 10):  # Change 200 to scrape fewer pages
  ```

- Random delays of **1.5–4 seconds** are applied between requests to reduce server load and avoid rate limiting.

---

## Responsible Scraping

- Yelp's [Terms of Service](https://www.yelp.com/static?p=tos) restrict automated scraping. This project was built for **academic/educational purposes** only as part of a university data analytics course.
- Randomized delays and page scrolling simulate normal user behavior to avoid overloading Yelp's servers.
- Do not use this spider for commercial data collection.
