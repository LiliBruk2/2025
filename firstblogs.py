import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from collections import defaultdict
from datetime import datetime

# Constants
BASE_URL = "https://www.hackeru.co.il"
BLOG_HOME = urljoin(BASE_URL, "/blog")
CATEGORY_PREFIX = "/blog/category/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_soup(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def extract_categories(soup):
    categories = []
    category_buttons = soup.find_all("a", href=True)
    for btn in category_buttons:
        href = btn['href']
        if href.startswith(CATEGORY_PREFIX):
            full_url = urljoin(BASE_URL, href)
            categories.append((btn.text.strip(), full_url))
    return list(set(categories))  # Remove duplicates if any

def extract_posts_from_category(category_name, category_url):
    soup = get_soup(category_url)
    posts = []
    articles = soup.find_all("article")
    for article in articles:
        a_tag = article.find("a", href=True)
        title = a_tag.get_text(strip=True)
        url = urljoin(BASE_URL, a_tag['href'])
        posts.append({
            "Title": title,
            "URL": url,
            "Category": category_name
        })
    return posts

def main():
    print("Fetching main blog page...")
    home_soup = get_soup(BLOG_HOME)

    print("Extracting categories...")
    categories = extract_categories(home_soup)

    all_posts = []
    url_to_categories = defaultdict(set)

    for name, url in categories:
        print(f"Scraping category: {name} ({url})")
        posts = extract_posts_from_category(name, url)
        for post in posts:
            url_to_categories[post["URL"].strip()].add(name)
            all_posts.append(post)

    # Deduplicate by URL and consolidate categories
    unique_posts = {}
    for post in all_posts:
        url = post["URL"].strip()
        if url not in unique_posts:
            unique_posts[url] = {
                "Title": post["Title"],
                "URL": url,
                "All Categories": ", ".join(sorted(url_to_categories[url])),
                "Multiple Categories?": "Yes" if len(url_to_categories[url]) > 1 else "No"
            }

    df = pd.DataFrame(unique_posts.values())
    summary = df["All Categories"].str.split(", ").explode().value_counts().reset_index()
    summary.columns = ["Category", "# of Posts"]

    # Save to Excel
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"blog_posts_{timestamp}.xlsx"
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="All Blog Posts", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    print(f"✅ Done! Exported to {filename}")

if __name__ == "__main__":
    main()
