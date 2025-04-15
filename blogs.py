import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import urllib3
import arabic_reshaper
from bidi.algorithm import get_display

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.hackeru.co.il"
BLOG_HOME = urljoin(BASE_URL, "/blog")
CATEGORY_PREFIX = "/blog/category/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_soup(url):
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def extract_categories(soup):
    categories = []
    for link in soup.find_all("a", href=True):
        href = link['href']
        if href.startswith(CATEGORY_PREFIX):
            full_url = urljoin(BASE_URL, href)
            reshaped = arabic_reshaper.reshape(link.text.strip())
            display_name = get_display(reshaped)
            categories.append((display_name, full_url))
    return list(set(categories))

def is_internal_link(href):
    return href.startswith("/") or href.startswith(BASE_URL)

def count_internal_links(article_url):
    try:
        soup = get_soup(article_url)
        links = soup.find_all("a", href=True)
        internal_links = [link['href'] for link in links if is_internal_link(link['href'])]
        return len(internal_links)
    except Exception:
        return 0

def extract_articles(category_name, category_url):
    soup = get_soup(category_url)
    posts = []
    post_cards = soup.select("a.post-card")
    for card in post_cards:
        title_element = card.select_one(".post-card__title h3")
        if title_element:
            post_title = title_element.get_text(strip=True)
            post_url = urljoin(BASE_URL, card['href'])
            internal_links = count_internal_links(post_url)
            posts.append({
                "Category": category_name,
                "Title": post_title,
                "URL": post_url,
                "# of Internal Links": internal_links
            })
    return posts

def main():
    print("🔍 Fetching blog homepage...")
    soup = get_soup(BLOG_HOME)

    print("📂 Extracting blog categories...")
    categories = extract_categories(soup)

    all_data = []
    for name, url in categories:
        print(f"📑 Scraping category: {name} ({url})")
        posts = extract_articles(name, url)
        if posts:
            all_data.extend(posts)
        else:
            print(f"⚠️ No blog posts found for category: {name}")

    if not all_data:
        print("⚠️ No data to export.")
        return None

    df = pd.DataFrame(all_data)
    summary_df = df.groupby("Category").agg(
        **{
            "# of Articles": ("Title", "count"),
            "Total Internal Links": ("# of Internal Links", "sum"),
        }
    ).reset_index()

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"blog_analysis_{timestamp}.xlsx"
    output_path = Path.cwd() / filename

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="All Posts", index=False)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

    print(f"\n✅ Done! Exported to {output_path}")
    return output_path

if __name__ == "__main__":
    main()
