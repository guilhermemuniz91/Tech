import requests
import time
from parsel import Selector
import re
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    headers = {"User-Agent": "Fake user-agent"}

    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    news = selector.css(".entry-title a::attr(href)").getall()
    return news


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.css(".next.page-numbers")
    if next_page:
        next_page_link = next_page.css("::attr(href)").get()
        return next_page_link
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css("h1.entry-title::text").get().strip("\xa0")
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".author a::text").get()
    reading_time = int(
        selector.css(".meta-reading-time::text").get().split(" ")[0]
    )
    summary = selector.css(".entry-content p").get()
    summary = re.sub("<.*?>", "", summary).strip()
    category = selector.css(".label::text").get()
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    news_list = []
    url = "https://blog.betrybe.com/"
    while len(news_list) < amount:
        response = fetch(url)
        updates = scrape_updates(response)
        news_list.extend(updates)
        url = scrape_next_page_link(response)
    arr_news_list = []
    for news in news_list[:amount]:
        scrap_news = scrape_news(fetch(news))
        arr_news_list.append(scrap_news)
    create_news(arr_news_list)
    return arr_news_list[:amount]
